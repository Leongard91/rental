from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('login', views.login, name='longin'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name="register")
]