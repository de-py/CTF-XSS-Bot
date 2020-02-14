from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="register/login.html"), name='login'),
    path('', views.register, name='register'),
]

