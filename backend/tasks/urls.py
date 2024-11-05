"""tasks urls module"""

# django
from django.urls import path

# local
from . import views


urlpatterns = [
    path('tasks-list/', views.TaskListView.as_view(), name='tasks_list'),
    path('tasks-detail/<int:pk>/', views.TaskDetailView.as_view(), name='tasks_detail'),
    path('tasks-list-pending/', views.TaskListPendingView.as_view(), name='tasks_list_pending'),
]