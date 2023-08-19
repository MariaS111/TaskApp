from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'board', views.BoardViewSet, basename='board')

urlpatterns = [
    path('', include(router.urls))
    # path('api/tasks/', views.TaskViewSet.as_view({'get': 'list'})),
    # path('api/tasks/create', views.TaskViewSet.as_view({'post': 'create'})),
    # path('api/tasks/<int:pk>/update/', views.TaskViewSet.as_view({'put': 'update'})),
    # path('api/tasks/<int:pk>/', views.TaskViewSet.as_view({'get': 'retrieve'})),
    # path('api/tasks/<int:pk>/delete/', views.TaskViewSet.as_view({'delete': 'destroy'})),
]
