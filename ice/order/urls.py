from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.user_profile, name='profile'),
    path('detail', views.view_detail, name='detail'),
    path('cart/', views.cart, name='cart'),
    path('buy/', views.buy, name='buy'),
    path('delete/', views.delete_item, name='delete'),
    path('show_cart', views.show_cart, name='show_cart'),
    path('show_buy', views.show_buy, name='show_buy'),
    path('search/', views.search, name='search'),
    path('change/', views.change_pass, name='change'),
    path('category/', views.category_filter, name='category'),
    path('statistics/', views.statistics_manager, name='statistics'),
    path('view_statistics/', views.view_statistics, name='view_statistics'),
    path('add_ice/', views.add_ice, name='add_ice'),
    path('add_form/', views.add_form, name='add_form'),
    path('delete_ice/', views.delete_ice, name='delete_ice'),
    path('show_edit_form/', views.show_edit_form, name='show_edit_form'),
    path('edit_ice_cream/', views.edit_ice_cream, name='edit_ice_cream'),
]