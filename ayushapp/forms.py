from django import forms
from .models import TaskModel
class TaskForm(forms.ModelForm):
	due= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

	class Meta:
		model = TaskModel
		fields = ['task','due']

