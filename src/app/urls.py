from django.urls import path
from .views import TaskList, TaskDetail, CreateTask, UpdateTask, DeleteTask, Login, Register
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('', TaskList.as_view(), name='task'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task_detail'),
    path('delete/<int:pk>', DeleteTask.as_view(), name='task_delete'),
    path('create-task', CreateTask.as_view(), name='create_task'),
    path('edit/<int:pk>', UpdateTask.as_view(), name='task_edit')
]
