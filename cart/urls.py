from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('remove_from_cart/<str:pk>', views.remove_from_cart, name='remove_from_cart'),
]
