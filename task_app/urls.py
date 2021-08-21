from django.urls import path
from .views import *

app_name = "chat"
urlpatterns = [
   path('login/', Login.as_view()),
   path('logout/', Logout.as_view()),
   path('registration/', Registration.as_view()),

   path('get_user_info/', GetUsername.as_view()),
   path('get_user_groups/', GetGroups.as_view()),
   path('get_user_mini_groups/', GetMiniGroups.as_view()),
   path('create_group/', CreateTaskGroup.as_view()),
   path('create_task/', createTask),
   path('update_photo/', UpdatePhoto.as_view()),
   path('update_task/', UpdateTask.as_view()),
   path('update_group/', UpdateGroup.as_view()),
]