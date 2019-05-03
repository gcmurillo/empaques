from django.urls import path, include
from .views import *

urlpatterns = [
    # API endpoints
    path('', API_index),
    # clases
    path('clases/', ClaseList.as_view()),
    path('clases/<int:pk>/', ClaseDetail.as_view()),
    # tipos_empaques
    path('tipo_empaques/', TipoEmpaqueList.as_view()),
    path('tipo_empaques/<int:pk>/', TipoEmpaqueDetail.as_view()),
    # estado_empaques
    path('estado_empaques/', EstadoEmpaqueList.as_view()),
    path('estado_empaques/<int:pk>/', EstadoEmpaqueDetail.as_view()),
    # marcas
    path('marcas/', MarcasList.as_view()),
    path('marcas/<int:pk>/', MarcasDetail.as_view()),
    # modelos
    path('modelos/', ModeloList.as_view()),
    path('modelos/<int:pk>/', ModeloDetail.as_view()),
    # ubicaciones
    path('ubicaciones/', UbicacionList.as_view()),
    path('ubicaciones/<int:pk>/', UbicacionDetail.as_view()),
    # empresas
    path('empresas/', EmpresaList.as_view()),
    path('empresas/<pk>', EmpresaDetail.as_view()),  # por codigo de empresa
    # representantes
    path('representantes/', RepresentanteList.as_view()),
    path('representantes/<int:pk>/', RepresentanteDetail.as_view()),
    # vendedores
    path('vendedores/', VendedorList.as_view()),
    # custodios
    path('custodios/', CustodioList.as_view()),
    path('custodios/<int:pk>/', CustodioDetail.as_view()),
    # empaques
    path('empaques/', EmpaquesList.as_view()),
    path('empaques/<pk>', EmpaquesDetail.as_view()),
]