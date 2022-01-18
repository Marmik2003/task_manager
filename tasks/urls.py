from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('add-task/', views.add_task, name='add_task'),
    path('complete_task/<int:pk>/', views.complete_task, name='complete_task'),
    path('completed_tasks/', views.completed_tasks, name='completed_tasks'),
    path('delete-task/<int:pk>/', views.delete_task, name='delete_task'),
    path('all_tasks/', views.all_tasks, name='all_tasks'),
]