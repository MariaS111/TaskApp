from django.shortcuts import render
from .models import Profile
from rest_framework.generics import RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, ProfileSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class TaskApiGet(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer