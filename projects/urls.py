from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'teamboard/(?P<teamboard_pk>\d+)/teamtask/(?P<teamtask_pk>\d+)/comments', views.CommentViewSet, basename='comments')
router.register(r'project', views.ProjectViewSet, basename='project')


urlpatterns = [
    path('', include(router.urls)),
]
