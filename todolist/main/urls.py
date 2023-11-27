from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as v
urlpatterns=[
   path('accounts/login/',v.LoginView.as_view(template_name='registration/login.html'),name='login'),
   path('accounts/logout/',v.LogoutView.as_view(),name='logout'),
   path('register/new/user/',views.CreateUserView.as_view(),name='sign_up'),
   path('',views.TaskManagerView.as_view(),name='tasks_manager'),
   path('new/',views.CreateTaskManager.as_view(),name='new'),
   path('task/<int:pk>/delete/',views.DeleteTaskManagerView.as_view(),name='delete_task_manager'),
   path('task/<int:pk>/edit/',views.EditTaskManagerView.as_view(),name='edit_task_manager'),
   path('task/<int:pk>/list/',views.TaskManagerDetailsView.as_view(),name='task_list'),
   path('create/task/<int:pk>/',views.TaskCreateView.as_view(),name='task_create'),
   path('update-task/<int:pk>',views.EditTaskView.as_view(),name='task_update'),
   path('delete-task/<int:pk>/',views.DeleteTaskView.as_view(),name='task_delete'),
   path('update_task_status/<int:pk>/',views.UpdateTaskStatusView.as_view,name='updated_task_status'),
]  