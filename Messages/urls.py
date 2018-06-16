from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', auth_views.login,name='login'),
    path('logout', auth_views.logout, name='logout'),
    path('directMessaging', views.directMessaging, name='directMessaging'),
    url(r'^directMessaging/$', views.directMessaging, name='directMessaging'),
    path('sendDirect', views.sendDirect, name='sendDirect'),
]