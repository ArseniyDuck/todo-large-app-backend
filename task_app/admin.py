from django.contrib import admin
from .models import TaskGroup, Task, User

admin.site.register(TaskGroup)
admin.site.register(Task)
admin.site.register(User)