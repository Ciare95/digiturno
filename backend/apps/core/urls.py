from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListarServiciosView, ListarSucursalesView, ServicioAdminViewSet

# Crear el router para los endpoints de administración
router = DefaultRouter()
router.register(r'admin/servicios', ServicioAdminViewSet)

urlpatterns = [
    # Rutas para servicios
    path('servicios/', ListarServiciosView.as_view(), name='listar_servicios'),
    
    # Rutas para sucursales
    path('sucursales/', ListarSucursalesView.as_view(), name='listar_sucursales'),

    # Incluir rutas del router
    path('', include(router.urls)),
]
