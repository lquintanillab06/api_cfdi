from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_user/', views.get_user, name='get_user'),
    path('get_usuario/', views.GetUser.as_view(), name='get_usuario'),
    path('auth_test/', views.test, name='test'),
]
