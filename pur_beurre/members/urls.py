from django.urls import path
# from .views import UserRegisterView, UserLoginView
from . import views


urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView, name='login'),
]
