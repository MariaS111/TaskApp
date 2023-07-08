from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_routes, name='routes'),
    path('tasks/', views.get_tasks, name='tasks'),
    path('tasks/<str:pk>/update/', views.update_task, name='task-update'),
    path('tasks/<str:pk>/', views.get_task, name='task')
]