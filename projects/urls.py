from django.urls import path, include
from . import views
from tasks.views import TeamTaskViewSet, CommentViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'project', views.ProjectViewSet, basename='project')
router.register(r'project/(?P<project_pk>\d+)/teamboard', views.ProjectTeamBoardViewSet, basename='project_teamboard')
router.register(r'project/(?P<project_pk>\d+)/teamboard/(?P<teamboard_pk>\d+)/teamtask', views.ProjectTeamTaskViewSet, basename='project_teamtask')
router.register(r'project/(?P<project_pk>\d+)/teamboard/(?P<teamboard_pk>\d+)/teamtask/(?P<teamtask_pk>\d+)/comments', CommentViewSet, basename='project_comments')

urlpatterns = [
    path('', include(router.urls)),
]
