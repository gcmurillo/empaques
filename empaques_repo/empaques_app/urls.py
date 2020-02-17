from django.urls import path, include
from .views import *

urlpatterns = [
    # API endpoints
    path('', API_index),
    path('login/', LoginView.as_view()),
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
    path('correos/', CorreoList.as_view()),
    # vendedores
    path('vendedores/', VendedorList.as_view()),
    # custodios
    path('custodios/crear/', CustodioCreate.as_view()),
    path('custodios/', CustodioDetail.as_view()),
    # empaques
    path('empaques/', EmpaquesList.as_view()),
    path('empaques/disponibles/', EmpaqueSelectable.as_view()),
    path('empaques/crear/', EmpaquesCreate.as_view()),
    path('empaques/<pk>/', EmpaquesDetail.as_view()),
    path('empaques/llenar/<pk>/', llenar_empaque),
    path('empaques/crear/upload/', UpdateCilindros.as_view()),
    path('empaquesFiltrado/', EmpaquesFiltered.as_view()),
    # ordenes
    path('tipo_ordenes/', TipoOrdenList.as_view()),
    path('ordenes/', OrdenList.as_view()),
    path('ordenes/crear/', OrdenCreate.as_view()),
    path('ordenes/despachar/<int:pk>/', despachar),
    path('ordenes/por_vencer', get_ordenes_por_caducar),
    path('ordenesFiltrado/', OrdenFiltered.as_view()),
    # ordenDetail
    path('ordenes/empaques/', OrdenEmpaqueDetailList.as_view()),
    path('ordenes/empaques/enlace/', OrdenEmpaqueDetailCreate.as_view()),
    path('ordenes/empaques/<int:pk>/', OrdenEmpaqueDetailUpdate.as_view()),
    path('ordenes/empaques/por_entregar/', OrdenEmpaqueDetailPorEntregar.as_view()),
    path('ordenes/empaques/filtro/', OrdenEmpaquesFiltered.as_view())
]
