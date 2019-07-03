from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('index_list/', views.index_list, name='index_list'),
    path('upload/', views.upload, name='upload')
]
