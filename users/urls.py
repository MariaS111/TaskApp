from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)
from users.views import MyTokenObtainPairView, AvatarUpdateView, UserProfileView, RegisterView, VerifyEmail, \
    UsersAllView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include('rest_social_auth.urls_jwt_pair')),
    # re_path('', include('social_django.urls', namespace='social')),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='verify_email'),
    path('all_users/', UsersAllView.as_view(), name='all_users'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/avatar-update/', AvatarUpdateView.as_view(), name='avatar_update'),
]