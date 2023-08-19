from django.shortcuts import render
from rest_framework import generics
from .models import Profile, CustomUser
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, ProfileSerializer, RegistrationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        return Profile.objects.get(user=user)