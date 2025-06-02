from django.urls import path
from .views import CrearTurnoView, ListarTurnosUsuarioView, DetalleTurnoUsuarioView

urlpatterns = [
    # Rutas para turnos
    path('turnos/', CrearTurnoView.as_view(), name='crear_turno'),
    path('mis-turnos/', ListarTurnosUsuarioView.as_view(), name='listar_turnos_usuario'),
    path('mis-turnos/<int:pk>/', DetalleTurnoUsuarioView.as_view(), name='detalle_turno_usuario'),
]