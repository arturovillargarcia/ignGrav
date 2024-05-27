from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualizador, name='visualizador'),
    path('info/', views.info, name='info'),
]