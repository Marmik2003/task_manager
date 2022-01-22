from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('pending/', views.PendingTaskView.as_view(), name='pending'),
    path('completed/', views.CompletedTaskView.as_view(), name='completed'),
    path('add/', views.AddTaskView.as_view(), name='add'),
    path('edit/<int:pk>/', views.EditTaskView.as_view(), name='edit'),
    path('delete/<int:id>/', views.DeleteTaskView.as_view(), name='delete'),
]
