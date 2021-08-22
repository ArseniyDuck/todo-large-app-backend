import datetime
import json
from urllib.parse import urlencode

from django.http import HttpResponse
from rest_framework.response import Response
from django.http import QueryDict

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.views import APIView
from django.views.generic import View
from rest_framework.decorators import api_view

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .serializers import GroupSerializer, UserSerializer, UserPhotoSerializer, TaskSerializer, MiniGroupSerializer
from .models import Task, TaskGroup
from .serializers import TaskValidator
from .forms import TaskGroupForm, RegisterForm, UpdateGroupForm, UpdatePhotoForm, UpdateTaskNameForm


class GetUsername(APIView):
   def get(self, request):
      if request.user.is_authenticated:
         serializer = UserSerializer(request.user)
         return Response(serializer.data)
      return HttpResponse(status=400)


class GetGroups(APIView):
   def get(self, request):
      groups = TaskGroup.objects.filter(user=request.user)
      serializer = GroupSerializer(groups, many=True, context={'filter_string': request.query_params.get('filter')})
      return Response(serializer.data)


class GetMiniGroups(APIView):
   def get(self, request):
      mini_groups = TaskGroup.objects.filter(user=request.user)
      serializer = MiniGroupSerializer(mini_groups, many=True)
      return Response(serializer.data)


class CreateTaskGroup(APIView):
   @method_decorator(ensure_csrf_cookie)
   def post(self, request):
      form = TaskGroupForm(data=request.data)
      if form.is_valid():
         group = TaskGroup.objects.create(
            name=form.cleaned_data['name'],
            user=request.user
         )
         serializer = MiniGroupSerializer(group)
         return Response(serializer.data, status=201)
      return HttpResponse(status=400)


class Login(View):
   @method_decorator(ensure_csrf_cookie)
   def post(self, request):
      form = AuthenticationForm(data=json_to_query_dict(request.body))
      if form.is_valid():
         login(request, form.get_user())
         return HttpResponse(status=201)
      else:
         return HttpResponse(status=400)


class Registration(View):
   @method_decorator(ensure_csrf_cookie)
   def post(self, request):
      form = RegisterForm(data=json_to_query_dict(request.body))
      if form.is_valid():
         user = form.save()
         login(request, user)
         return HttpResponse(status=201)
      else:
         print(form.errors)
         return HttpResponse(status=400)


class Logout(View):
    def get(self, request):
      if request.user.is_authenticated:
         logout(request)
         return HttpResponse(status=200)
      return HttpResponse(status=400)


class UpdatePhoto(APIView):
   @method_decorator(ensure_csrf_cookie)
   def post(self, request):
      if request.user.is_authenticated:
         form = UpdatePhotoForm(request.POST, request.FILES)
         if form.is_valid():
            request.user.photo = form.cleaned_data['photo']
            request.user.save()
            serializer = UserPhotoSerializer(request.user)
            return Response(serializer.data, status=201)
         return HttpResponse(status=400)
      return HttpResponse(status=400)


class UpdateTask(APIView):
   def serialize_task(self, task):
      serializer = TaskSerializer(task)
      return serializer.data

   @method_decorator(ensure_csrf_cookie)
   def post(self, request):
      post_data = QueryDict(urlencode(request.data))
      hasName, hasDeadline, hasAction = post_data.__contains__('name'), post_data.__contains__('deadline'), post_data.__contains__('action')
      if hasName or hasDeadline or hasAction:
         form = UpdateTaskNameForm(data=post_data)
         if form.is_valid():
            task = Task.objects.get(pk=post_data.get('id'))
            if task.task_group.user == request.user:
               if hasAction:
                  actionString = post_data.get('action')
                  if actionString == 'complete':
                     task.is_completed = True
                  elif actionString == 'delete':
                     task.delete()
                     return HttpResponse(status=204)
               if hasName:
                  task.name = post_data.get('name')
               if hasDeadline:
                  task.deadline=strptime(post_data.get('deadline'))
               task.save()
               return Response(self.serialize_task(task), status=201)
            return HttpResponse(status=400)
         return HttpResponse(status=400)
      return HttpResponse(status=400)


class UpdateGroup(APIView):
   def serialize_task(self, task):
      serializer = MiniGroupSerializer(task)
      return serializer.data

   @method_decorator(ensure_csrf_cookie)
   def post(self, request):
      post_data = QueryDict(urlencode(request.data))
      hasName, hasAction = post_data.__contains__('name'), post_data.__contains__('action')
      if hasName or hasAction:
         form = UpdateGroupForm(data=post_data)
         if form.is_valid():
            group = TaskGroup.objects.get(pk=post_data.get('id'))
            if group.user == request.user:
               if hasAction:
                  actionString = post_data.get('action')
                  if actionString == 'delete':
                     group.delete()
                     return HttpResponse(status=204)
               if hasName:
                  group.name = post_data.get('name')
               group.save()
               return Response(self.serialize_task(group), status=201)
            return HttpResponse(status=400)
         return HttpResponse(status=400)
      return HttpResponse(status=400)


@ensure_csrf_cookie
@api_view(['POST'])
def createTask(request):
   ser_data = TaskValidator(data=request.data)
   if ser_data.is_valid():
      task = Task.objects.create(
         deadline=strptime(ser_data.validated_data.get('deadline')),
         name=ser_data.validated_data.get('taskname'),
         task_group=TaskGroup.objects.get(id=ser_data.validated_data.get('group_id')),
      )
      serializer = TaskSerializer(task)
      return Response(serializer.data, status=201)
   else:
      print(ser_data.errors)
   return HttpResponse(status=400)


def json_to_query_dict(body):
   return QueryDict(urlencode(json.loads(body)))


def strptime(time):
   return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M')