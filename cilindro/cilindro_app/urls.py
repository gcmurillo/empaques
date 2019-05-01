from django.urls import path, include
from .views import *

urlpatterns = [
    # API endpoints
    path('', API_index),
    path('clases/', ClaseList.as_view()),
    path('clases/<int:pk>/', ClaseDetail.as_view()),
    path('tipo_empaques/', TipoEmpaqueList.as_view()),
    path('tipo_empaques/<int:pk>/', TipoEmpaqueDetail.as_view()),
    path('estado_empaques/', EstadoEmpaqueList.as_view()),
    path('estado_empaques/<int:pk>/', EstadoEmpaqueDetail.as_view()),
    path('marcas/', MarcasList.as_view()),
    path('marcas/<int:pk>/', MarcasDetail.as_view()),
    path('modelos/', ModeloList.as_view()),
    path('modelos/<int:pk>/', ModeloDetail.as_view()),
    path('ubicaciones/', UbicacionList.as_view()),
    path('ubicaciones/<int:pk>/', UbicacionDetail.as_view()),
]