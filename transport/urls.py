from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name="register"), 
    path('offers', views.get_offers, name='offers'),
    path('add_offer', views.add_offer, name='add_offer'), 
    path('search', views.search_view, name='search'),
    path('filter', views.offer_filter, name='filter'),
    path('details/<int:transport_id>', views.details_view, name='details'),
    path('user/<int:id>', views.user_view, name='user_page')
]