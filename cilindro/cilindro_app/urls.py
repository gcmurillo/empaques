from django.urls import path, include
from .views import *

urlpatterns = [
    path('clases/', clase_list),
    path('clases/<int:pk>/', clase_detail),
]