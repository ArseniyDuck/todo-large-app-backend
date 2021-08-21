from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import TaskGroup, Task, User


class TaskSerializer(serializers.ModelSerializer):
   created_at = serializers.CharField(source='created_at_to_string') 
   timedelta = serializers.CharField(source='calculate_timedelta')
   task_type = serializers.CharField(source='calculate_type')
   deadline = serializers.CharField(source='deadline_to_string')

   class Meta:
      model = Task
      fields = ('id', 'is_completed', 'name', 'task_type', 'deadline', 'created_at', 'task_group', 'timedelta')


class GroupSerializer(serializers.ModelSerializer):
   tasks = SerializerMethodField('get_filtered_tasks')

   def get_filtered_tasks(self, obj):
      filter_string = self.context['filter_string']

      if filter_string is not None and type(filter_string) is str and len(filter_string) > 0:
         return TaskSerializer(obj.get_filtered_tasks(filter_string), many=True).data

      elif (type(filter_string) is str and len(filter_string) == 0) or (filter_string is None):
         return TaskSerializer(obj.tasks_set.all(), many=True).data

      else:
         print('GroupFilterSerializerError occured!')
         

   class Meta:
      model = TaskGroup
      fields = ('id', 'name', 'tasks')


class MiniGroupSerializer(serializers.ModelSerializer):
   class Meta:
      model = TaskGroup
      fields = ('id', 'name', )


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ('username', 'photo')


class UserPhotoSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ('photo', )


class TaskValidator(serializers.Serializer):
   taskname = serializers.CharField(required=True, max_length=30)
   group_id = serializers.IntegerField(required=True)
   deadline = serializers.CharField(required=True, max_length=16)