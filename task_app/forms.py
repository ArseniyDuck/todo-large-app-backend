from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import TaskGroup, User, Task


class RegisterForm(UserCreationForm):
   class Meta:
      model = User
      fields = ('username', 'password1', 'password2', )


class UpdatePhotoForm(forms.ModelForm):
   class Meta:
      model = User
      fields = ('photo', )

   
class UpdateTaskNameForm(forms.ModelForm):
   class Meta:
      model = Task
      fields = ('id', )


class UpdateGroupForm(forms.ModelForm):
   class Meta:
      model = TaskGroup
      fields = ('id', )


class TaskGroupForm(forms.ModelForm):
   class Meta:
      model = TaskGroup
      fields = ('name', )