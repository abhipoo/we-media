from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateTopicForm, CreateContentForm, AskRecommendationForm, SuggestionForm, CreateCommentForm
from .models import Topic, content, content_types, ask, suggestion, Comment, Comment_relation
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#Create your views here.

#Homepage
def index(request):
    #return HttpResponse("Homepage, bitchh")
    return render(request, 'discuss/index.html')

#Topic app
def create_topic(request):
    #return HttpResponse("Create new discussion")
    if request.method == 'POST':
        form = CreateTopicForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.is_op = True
            post.save()

            #redirect to new created topic
            return view_topic(request, post.id) #Help - How to change URL to /discuss/topic_id
        else:
            print("Form invalid")
            print(form.errors)


    form = CreateTopicForm()

    context = {
        'form' : form
    }

    return render(request, 'discuss/create_topic.html', context)

def view_topic(request, topic_id):
    #return HttpResponse("View discussion for id " + str(topic_id))
    topic_object = Topic.objects.get(pk = topic_id)

    #form = CreateTopicForm()

    #points = get_points_of_topic(topic_id)

    #counterpoints = get_counterpoints_of_topic(topic_id)

    recommendations = get_recommendations_on_topic(topic_object)

    discussion_form = CreateCommentForm()

    discussions = topic_object.comments.all()

    context = {
        'topic' : topic_object,
        #'form' : form,
        #'points' : points,
        #'counterpoints' : counterpoints,
        'recommendations' : recommendations,
        'discussion_form' : discussion_form,
        'discussions' : discussions
    }

    return render(request, 'discuss/view_topic.html', context)


def show_all_topics(request):
    #return HttpResponse("Shows all topics")
    topics = Topic.objects.all()
    form = CreateTopicForm()
    context = {
    'topics' : topics,
    'form' : form
    }
    return render(request, 'discuss/all_topics.html', context)


#Content app
def create_content(request):
    #return HttpResponse("Create new discussion")
    if request.method == 'POST':
        form = CreateContentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            # Now, save the many-to-many data for the form.
            form.save_m2m()

            #redirect to new created content
            return view_content(request, post.id) #Help - How to change URL to /discuss/content/content_id
        else:
            #Todo - Send form.errors to show in frontend popup.
            print("Form invalid")
            print(form.errors)


    form = CreateContentForm()

    context = {
        'form' : form
    }

    return render(request, 'discuss/create_content.html', context)

def view_content(request, content_id):
    #return HttpResponse("View content for id " + str(content_id))

    content_object = content.objects.get(pk = content_id)

    topics = get_topics_of_recommendation(content_object)

    related_content = get_related_content(content_object)

    discussion_form = CreateCommentForm()

    discussions = content_object.comments.all()

    context = {
        'content' : content_object,
        'topics' : topics,
        'related_content' : related_content,
        'discussion_form' : discussion_form,
        'discussions' : discussions
    }

    return render(request, 'discuss/view_content.html', context)

def show_all_content(request):
    contents = ask.objects.all().order_by('-vote')
    context = {
    'asks' : contents,
    }
    return render(request, 'discuss/all_content.html', context)

#separate app - suggestions / recommendations
def ask_recommendation(request):
    #return HttpResponse("Ask for a content recommendation")
    if request.method=='POST':
        form = AskRecommendationForm(request.POST, request.FILES)
        if form.is_valid():
            ask_form = form.save()
            #ask_form.user = request.user
            try:
                img = request.FILES['img']
                ask_form.image = img
            except:
                pass
            ask_form.save()
            # ask_form.save()
            # form.save_m2m() # needed since using commit=False

            return view_ask(request, ask_form.id)
        else:
            print("Form invalid")
            print(form.errors)

    form = AskRecommendationForm()

    context = {
        'form' : form
    }

    return render(request, 'discuss/ask_recommendation.html', context)

def view_ask(request, ask_id):
    #return HttpResponse("Ask id" + str(ask_id))

    #ask_object = ask.objects.get(pk = ask_id)
    ask_object = get_object_or_404(ask, pk=ask_id)

    content_types = list(ask_object.content_choices.all().values_list('title', flat = True))

    form = SuggestionForm()

    suggestions = suggestion.objects.filter(ask_id = ask_id)

    context = {
        'ask' : ask_object,
        'content_types' : content_types,
        'form' : form,
        'suggestions' : suggestions
    }

    return render(request, 'discuss/view_ask.html', context)

@login_required
def vote_ask(request, ask_id, vote_type):
    a = ask.objects.get(id=ask_id)
    if a in request.user.profile.asks_voted.all():
        messages.error(request, "You have already Voted on this.")
        return view_ask(request, ask_id)

    request.user.profile.asks_voted.add(a)
    if vote_type == 'downvote':
        a.vote -= 1

    elif vote_type == 'upvote':
        a.vote += 1

    else:
        messages.error(request, "Seems Like an invalid response. Try again later.")
        return view_ask(request, ask_id)

    a.save()

    messages.success(request, "Your vote has been successfully registered.")
    return view_ask(request, ask_id)

def add_suggestion(request, ask_id):
    #return HttpResponse("Button for adding point")
    form = SuggestionForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.ask_id = ask_id #Check if this works after fixing class names - post.ask = ask_id
        post.save()
    else:
        print("Form invalid")
        print(form.errors)

    return view_ask(request, ask_id)

def show_all_asks(request):
    #return HttpResponse("Shows all content")
    form = AskRecommendationForm()
    context = {
        'form' : form
    }

    return render(request, 'discuss/all_asks.html', context)


#seperate app - discussions
def create_discussion(request):
    #return HttpResponse("Create new discussion")
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.is_op = True
            if request.user.is_authenticated:
                post.author = request.user
            #else:
                #redirect to login page
            post.save()

            #redirect to new created topic
            return view_discussion(request, post.id) #Help - How to change URL to /discuss/topic_id
        else:
            print("Form invalid")
            print(form.errors)

    form = CreateCommentForm()
    context = {
        'form' : form
    }

    return render(request, 'discuss/create_discussion.html', context)

def create_discussion_on_topic(request, topic_id):
    #return HttpResponse("Create new discussion")
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.is_op = True

            if request.user.is_authenticated:
                post.author = request.user

            post.save()

            #get topic from topic id
            topic_obj = Topic.objects.get(pk = topic_id)

            post.topics.add(topic_obj)

            #redirect to new created topic
            return view_discussion(request, post.id) #Help - How to change URL to /discuss/topic_id
        else:
            print("Form invalid")
            print(form.errors)

    form = CreateCommentForm()
    context = {
        'form' : form
    }

    return render(request, 'discuss/create_discussion.html', context)

def create_discussion_on_content(request, content_id):
    #return HttpResponse("Create new discussion")
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.is_op = True

            if request.user.is_authenticated:
                post.author = request.user

            post.save()

            #get topic from topic id
            content_obj = content.objects.get(pk = content_id)

            post.contents.add(content_obj)

            #redirect to new created topic
            return view_discussion(request, post.id) #Help - How to change URL to /discuss/topic_id
        else:
            print("Form invalid")
            print(form.errors)

    form = CreateCommentForm()
    context = {
        'form' : form
    }

    return render(request, 'discuss/create_discussion.html', context)


def view_discussion(request, comment_id):
    #return HttpResponse("View discussion for id " + str(topic_id))
    comment_object = Comment.objects.get(pk = comment_id)

    form = CreateCommentForm()

    points = get_points_of_comment(comment_id)

    counterpoints = get_counterpoints_of_comment(comment_id)

    parent_id = get_parent_comment_id(comment_id)

    #recommendations = get_recommendations_on_topic(topic_object)

    topics = comment_object.topics.all()

    contents = comment_object.contents.all()

    context = {
        'comment' : comment_object,
        'form' : form,
        'points' : points,
        'counterpoints' : counterpoints,
        'parent_id' : parent_id,
        'topics' : topics,
        'contents' : contents
        #'recommendations' : recommendations
    }

    return render(request, 'discuss/view_discussion.html', context)

def show_all_discussions(request):
    #return HttpResponse("Shows all content")
    discussions = Comment.objects.filter(is_op = 1)
    form = CreateCommentForm()
    context = {
        'discussions' : discussions,
        'form' : form
    }

    return render(request, 'discuss/all_discussions.html', context)


def add_point(request, comment_id):
    #return HttpResponse("Button for adding point")
    form = CreateCommentForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.is_op = False

        if request.user.is_authenticated:
            post.author = request.user

        post.save()

        add_relation(comment_id, post, 'P') #P denotes Point
    else:
        print("Form invalid")
        print(form.errors)

    return view_discussion(request, comment_id)


def add_counterpoint(request, comment_id):
    #return HttpResponse("Button for adding point")
    form = CreateCommentForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.is_op = False

        if request.user.is_authenticated:
            post.author = request.user

        post.save()

        add_relation(comment_id, post, 'CP') #CP denotes Counterpoint
    else:
        print("Form invalid")
        print(form.errors)

    return view_discussion(request, comment_id)


#helper functions
#def save_form():
#Persists CreateTopicForm

def get_recommendations_on_topic(topic_object):
    #Get list of contents on topic
    return topic_object.content_set.all()

def get_topics_of_recommendation(content_object):
    return content_object.topics.all()

def get_related_content(content_object):
    return content_object.related_content.all()

def add_relation(from_comment_id, to_comment, relation_type):
    #get source object #Help - Can this unnecessary call to DB be avoided ?
    from_comment = Comment.objects.get(pk = from_comment_id)

    #Persists relation between two entities
    r = Comment_relation(source = from_comment, target = to_comment, relation_type = relation_type)
    r.save()

def get_points_of_comment(source_id):
    #Get a list of point ids for a topic
    p_target_ids = list(Comment_relation.objects.filter(source = source_id).filter(relation_type = 'P').values_list('target', flat = True))
    #Returns query set of those point topics
    points = Comment.objects.filter(id__in = p_target_ids)

    return points

def get_counterpoints_of_comment(source_id):
    #Get a list of point ids for a topic
    cp_target_ids = list(Comment_relation.objects.filter(source = source_id).filter(relation_type = 'CP').values_list('target', flat = True))

    #Returns query set of those point topics
    counterpoints = Comment.objects.filter(id__in = cp_target_ids)

    return counterpoints

def get_parent_comment_id(comment_id):
    try: #Help - simpler querying
        return Comment_relation.objects.filter(target = comment_id).values('source').get()['source']
    except:
        return -1
