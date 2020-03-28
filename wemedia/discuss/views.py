from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateTopicForm, CreateContentForm
from .models import topic, relation, content

#Create your views here.
def create_topic(request):
    #return HttpResponse("Create new discussion")
    if request.method == 'POST':
        form = CreateTopicForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.is_op = True
            post.save()

            #redirect to new created topic
            return discuss(request, post.id) #Help - How to change URL to /discuss/topic_id
        else:
            print("Form invalid")
            print(form.errors)


    form = CreateTopicForm()

    context = {
        'form' : form
    }
    
    return render(request, 'discuss/create_topic.html', context)

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
            return discuss_content(request, post.id) #Help - How to change URL to /discuss/content/content_id
        else:
            print("Form invalid")
            print(form.errors)


    form = CreateContentForm()

    context = {
        'form' : form
    }
    
    return render(request, 'discuss/create_content.html', context)


def show_all_topics(request):
    #return HttpResponse("Shows all topics")
    topics = topic.objects.all()
    context = {'topics' : topics}
    return render(request, 'discuss/all_topics.html', context)

def show_all_content(request):
    #return HttpResponse("Shows all content")
    contents = content.objects.all()
    context = {'contents' : contents}
    return render(request, 'discuss/all_content.html', context)


def discuss(request, topic_id):
    #return HttpResponse("View discussion for id " + str(topic_id))
    topic_object = topic.objects.get(pk = topic_id)
    
    form = CreateTopicForm()

    points = get_points_of_topic(topic_id)

    counterpoints = get_counterpoints_of_topic(topic_id)

    recommendations = get_recommendations_on_topic(topic_object)

    context = {
        'topic' : topic_object,
        'form' : form, 
        'points' : points,
        'counterpoints' : counterpoints,
        'recommendations' : recommendations
    }

    return render(request, 'discuss/discuss.html', context)

def discuss_content(request, content_id):
    #return HttpResponse("View content for id " + str(content_id))

    content_object = content.objects.get(pk = content_id)

    topics = get_topics_of_recommendation(content_object)

    related_content = get_related_content(content_object)

    context = {
        'content' : content_object,
        'topics' : topics,
        'related_content' : related_content
    }

    return render(request, 'discuss/content.html', context)


def add_point(request, topic_id):
    #return HttpResponse("Button for adding point")
    form = CreateTopicForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.is_op = False
        post.save()

        add_relation(topic_id, post.id, 'P') #P denotes Point
    else:
        print("Form invalid")
        print(form.errors)

    return discuss(request, topic_id)


def add_counterpoint(request, topic_id):
    #return HttpResponse("Button for adding point")
    form = CreateTopicForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.is_op = False
        post.save()

        add_relation(topic_id, post.id, 'CP') #CP denotes Counterpoint
    else:
        print("Form invalid")
        print(form.errors)

    return discuss(request, topic_id)


#helper functions
#def save_form():
#Persists CreateTopicForm

def add_relation(from_topic_id, to_topic_id, relation_type):
    #Persists relation between two entities    
    r = relation(source_id = from_topic_id, target_id = to_topic_id, relation_type = relation_type)
    r.save()

def get_points_of_topic(source_id):
    #Get a list of point ids for a topic
    p_target_ids = list(relation.objects.filter(source_id = source_id).filter(relation_type = 'P').values_list('target_id', flat = True))
    
    #Returns query set of those point topics
    points = topic.objects.filter(id__in = p_target_ids)

    return points

def get_counterpoints_of_topic(source_id):
    #Get a list of point ids for a topic
    cp_target_ids = list(relation.objects.filter(source_id = source_id).filter(relation_type = 'CP').values_list('target_id', flat = True))
    
    #Returns query set of those point topics
    counterpoints = topic.objects.filter(id__in = cp_target_ids)

    return counterpoints

def get_recommendations_on_topic(topic_object):
    #Get list of contents on topic
    return topic_object.content_set.all()

def get_topics_of_recommendation(content_object):
    return content_object.topics.all()

def get_related_content(content_object):
    return content_object.related_content.all()