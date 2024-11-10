# tasks/urls.py
from django.urls import path
from .views import TaskListView, TaskDetailView

urlpatterns = [
    path('task-list/', TaskListView.as_view(), name='task_list'),
    path('task-detail/<int:id>/', TaskDetailView.as_view(), name='task_detail'),
]
