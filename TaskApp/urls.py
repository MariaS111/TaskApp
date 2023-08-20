from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)
from users.views import MyTokenObtainPairView, AvatarUpdateView, UserProfileView, RegisterView, VerifyEmail
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Task App API",
      default_version='v1',
      description="Task App",
      terms_of_service="https://www.taskapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@taskapp.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/verify-email/', VerifyEmail.as_view(), name='verify_email'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path('api/profile/avatar-update/', AvatarUpdateView.as_view(), name='avatar_update'),
    # re_path(r'^swagger(?P\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
