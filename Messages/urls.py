from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', auth_views.login,name='login'),
    path('sendMessage', views.sendMessage, name='sendMessage'),
]