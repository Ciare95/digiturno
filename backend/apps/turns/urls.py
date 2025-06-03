from django.urls import path
from .views import (
    CrearTurnoView, ListarTurnosUsuarioView, DetalleTurnoUsuarioView,
    CrearCalificacionView, ListarCalificacionesUsuarioView, DetalleCalificacionView,
    ListarTurnosAgendadosView
)

urlpatterns = [
    # Rutas para turnos
    path('turnos/', CrearTurnoView.as_view(), name='crear_turno'),
    path('mis-turnos/', ListarTurnosUsuarioView.as_view(), name='listar_turnos_usuario'),
    path('mis-turnos/<int:pk>/', DetalleTurnoUsuarioView.as_view(), name='detalle_turno_usuario'),
    path('turnos/agenda/', ListarTurnosAgendadosView.as_view(), name='listar_turnos_agenda'),
    
    # Rutas para calificaciones
    path('calificaciones/', ListarCalificacionesUsuarioView.as_view(), name='listar_calificaciones'),
    path('calificaciones/crear/', CrearCalificacionView.as_view(), name='crear_calificacion'),
    path('calificaciones/<int:pk>/', DetalleCalificacionView.as_view(), name='detalle_calificacion'),
]