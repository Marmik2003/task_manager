from django.urls import path
from rest_framework_nested import routers
from .api.views import TaskViewSet, TaskHistoryViewSet
from . import views

app_name = 'tasks'

router = routers.DefaultRouter()
router.register(r'api/tasks', TaskViewSet, basename='tasks')

history_router = routers.NestedSimpleRouter(router, r'api/tasks', lookup='task')
history_router.register(r'history', TaskHistoryViewSet, basename='history')

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('pending/', views.PendingTaskView.as_view(), name='pending'),
    path('completed/', views.CompletedTaskView.as_view(), name='completed'),
    path('add/', views.AddTaskView.as_view(), name='add'),
    path('edit/<int:pk>/', views.EditTaskView.as_view(), name='edit'),
    path('delete/<int:id>/', views.DeleteTaskView.as_view(), name='delete'),
    path('schedule_reports/', views.TaskReportView.as_view(), name='schedule_reports'),
] + router.urls + history_router.urls
