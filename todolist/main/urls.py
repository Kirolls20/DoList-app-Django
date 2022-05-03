from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as v
urlpatterns=[
   path('accounts/login/',v.LoginView.as_view(template_name='registration/login.html'),name='login'),
   path('accounts/logout/',v.LogoutView.as_view(),name='logout'),
   path('register/new/user/',views.CreateUserView.as_view(),name='sign_up'),
   path('',views.TaskList.as_view(),name='task_list'),
   path('create/task/',views.TaskCreateView.as_view(),name='task_create'),
   path('update-task/<int:pk>',views.TaskEditView.as_view(),name='task_update'),
   path('delete-task/<int:pk>/',views.TaskDeleteView.as_view(),name='task_delete'),
]