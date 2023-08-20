from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)
from users.views import MyTokenObtainPairView, AvatarUpdateView, UserProfileView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path('api/profile/avatar-update/', AvatarUpdateView.as_view(), name='avatar-update')
]
