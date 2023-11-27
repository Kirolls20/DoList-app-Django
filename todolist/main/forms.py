from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task, TaskManager

class CreateUserForm(UserCreationForm):
   full_name=forms.CharField(max_length=200)

   class Meta:
      model= User
      fields=['full_name','username', 'email']

class CreateTasksForm(forms.ModelForm):

   class Meta:
      model = Task
      fields =['title','description','complete']