from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, CustomUser
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, ProfileSerializer, RegistrationSerializer, CustomUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class UserProfileView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class AvatarUpdateView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.userprofile

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save(user=instance.user)