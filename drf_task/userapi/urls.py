from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, UserInfoView, UserUpdateView
from rest_framework_simplejwt import views as jwt_views

app_name = 'userapi'

urlpatterns = [
    path('users/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='register'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('users/<int:pk>/', UserInfoView.as_view()),
    path('users/update/<int:pk>/', UserUpdateView.as_view()),
]