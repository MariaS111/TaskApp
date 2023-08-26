from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'board', views.BoardViewSet, basename='board')
router.register(r'board/(?P<board_pk>\d+)/task', views.TaskViewSet, basename='task')
router.register(r'teamboard', views.TeamBoardViewSet, basename='teamboard')
router.register(r'teamboard/(?P<teamboard_pk>\d+)/teamtask', views.TeamTaskViewSet, basename='teamtask')

urlpatterns = [
    path('', include(router.urls)),
    # path('board/<int:pk>/done_tasks/', views.BoardViewSet.as_view({'get': 'done_tasks'}), name='board-done-tasks'),
    # path('api/tasks/', views.TaskViewSet.as_view({'get': 'list'})),
    # path('api/tasks/create', views.TaskViewSet.as_view({'post': 'create'})),
    # path('api/tasks/<int:pk>/update/', views.TaskViewSet.as_view({'put': 'update'})),
    # path('api/tasks/<int:pk>/', views.TaskViewSet.as_view({'get': 'retrieve'})),
    # path('api/tasks/<int:pk>/delete/', views.TaskViewSet.as_view({'delete': 'destroy'})),
]
