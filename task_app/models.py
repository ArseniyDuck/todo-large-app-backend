from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
   photo = models.ImageField(upload_to='photos/', blank=True)


class TaskGroup(models.Model):
   name = models.CharField(max_length=30)
   user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name='task_groups'
   )

   def get_filtered_tasks(self, filter_string):
      return self.tasks_set.filter(name__contains=filter_string)

   def __str__(self):
      return self.name


class Task(models.Model):
   name = models.CharField(max_length=30)
   is_completed = models.BooleanField(default=False)
   task_group = models.ForeignKey(
      TaskGroup,
      on_delete=models.CASCADE,
      related_name='tasks_set'
   )
   deadline = models.DateTimeField()
   created_at = models.DateTimeField(auto_now_add=True, editable=False)

   def calculate_timedelta(self):
      delta = self.deadline - self.created_at
      return delta

   def calculate_type(self):
      timedelta = self.calculate_timedelta()
      if timedelta.days:
         if timedelta.days > 7:
            return 'Monthly'
         return 'Weekly'
      return 'Daily'

   def deadline_to_string(self):
      return self.deadline.strftime('%Y-%m-%dT%H:%M') 

   def created_at_to_string(self):
      return self.created_at.strftime('%Y-%m-%d %H:%M')
      
   def __str__(self):
      return self.name
