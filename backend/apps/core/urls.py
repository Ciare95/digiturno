from django.urls import path
from .views import ListarServiciosView, ListarSucursalesView

urlpatterns = [
    # Rutas para servicios
    path('servicios/', ListarServiciosView.as_view(), name='listar_servicios'),
    
    # Rutas para sucursales
    path('sucursales/', ListarSucursalesView.as_view(), name='listar_sucursales'),
]
