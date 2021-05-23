from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name="register"), 
    path('offers', views.get_offers, name='offers'),
    path('add_offer', views.add_offer, name='add_offer'), 
    path('offer/<int:offer_id>', views.offer_view, name="offer_page"),
    path('search', views.search_view, name='search'), # delete in the end
    path('filter', views.offer_filter, name='filter')
]