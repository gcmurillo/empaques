from django.urls import path, include
from .views import *

urlpatterns = [
    path('clases/', clase_list),
    path('clases/<int:pk>/', clase_detail),
    path('tipo_empaques/', tipo_empaque_list),
    path('tipo_empaques/<int:pk>/', tipo_empaque_detail),
]