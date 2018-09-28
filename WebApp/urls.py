from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('interpreter/', views.interpreter, name='interpreter'),
   path('result/', views.result, name='result'),
]