from django import forms
from .models import topic, content

class CreateTopicForm(forms.ModelForm):
	class Meta:
		model = topic
		exclude = ('is_op',)

class CreateContentForm(forms.ModelForm):
	class Meta:
		model = content
		exclude = ('contexts',)
