from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.api import user

urlpatterns = [
    # User
    path('register/', user.RegisterUser.as_view(), name='register'),
    path('users/', user.GetAllUsers.as_view(), name='users'),
    path('users/<int:pk>/', user.GetUserById.as_view(), name='user_details'),

    # JWT 
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
