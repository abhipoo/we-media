from django import forms
from .models import Topic, content, content_types, ask, suggestion, Comment

class CreateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('description',)

class CreateContentForm(forms.ModelForm):  
    class Meta:
        model = content
        exclude = ('contexts', 'topics', 'related_content', 'creator')

    '''
    def clean(self):
        cleaned_data = super(CreateContentForm, self).clean()
        title = cleaned_data.get("title")
        creator = cleaned_data.get("creator")

        if not title and not creator:  # This will check for None or Empty
            raise forms.ValidationError('Even one of title or creator should have a value.')
    '''

#separate app - Suggestions
class AskRecommendationForm(forms.ModelForm):
    content_choices = forms.ModelMultipleChoiceField(queryset=content_types.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ask
        exclude = ('',)

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = suggestion
        exclude = ('ask', )

#separate app - Discussions
class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_op', 'topics', 'contents')
