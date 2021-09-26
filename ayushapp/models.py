from django.db import models
from django.contrib.auth.models import User

class TaskModel(models.Model):
	us = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	
	task=models.CharField(max_length=200)
	time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	due = models.DateField(auto_now_add=False, auto_now=False, blank=True,null=True)
	def __str__(self):
		return self.task