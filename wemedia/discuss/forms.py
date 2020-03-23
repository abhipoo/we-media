from django import forms
from .models import topic

class CreateTopicForm(forms.ModelForm):
	class Meta:
		model = topic
		exclude = ('is_op',)
