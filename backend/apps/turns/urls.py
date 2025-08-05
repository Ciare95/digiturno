from django.urls import path
from .views import (
    CrearTurnoView, 
    ListarTurnosUsuarioView, 
    DetalleTurnoUsuarioView,
    CrearCalificacionView, 
    ListarCalificacionesUsuarioView, 
    DetalleCalificacionView,
    ListarTurnosAgendadosView, 
    HistorialTurnosView,
    SiguienteTurnoEmpleadoView, 
    CompletarTurnoEmpleadoView, 
    TransferirTurnoEmpleadoView,
    TurnoActualEmpleadoView, 
    ListarColaTurnosEmpleadoView, 
    EstadisticasEmpleadoView,
    ListarColaTurnosView,
    IniciarAtencionView,
    FinalizarAtencionView,
    UltimosTurnosFinalizadosView
)

urlpatterns = [
    # Rutas para turnos
    path('turnos/', CrearTurnoView.as_view(), name='crear_turno'),
    path('mis-turnos/', ListarTurnosUsuarioView.as_view(), name='listar_turnos_usuario'),
    path('mis-turnos/<int:pk>/', DetalleTurnoUsuarioView.as_view(), name='detalle_turno_usuario'),
    path('turnos/agenda/', ListarTurnosAgendadosView.as_view(), name='listar_turnos_agenda'),
    path('turnos/historial/', HistorialTurnosView.as_view(), name='historial_turnos'),
    path('turnos/cola/', ListarColaTurnosView.as_view(), name='listar_cola_turnos'),
    
    # Rutas para calificaciones
    path('calificaciones/', ListarCalificacionesUsuarioView.as_view(), name='listar_calificaciones'),
    path('calificaciones/crear/', CrearCalificacionView.as_view(), name='crear_calificacion'),
    path('calificaciones/<int:pk>/', DetalleCalificacionView.as_view(), name='detalle_calificacion'),

    # Rutas para la gestión de turnos por empleados
    path('empleado/turnos/siguiente/', SiguienteTurnoEmpleadoView.as_view(), name='siguiente_turno_empleado'),
    path('empleado/turnos/<int:turno_id>/completar/', CompletarTurnoEmpleadoView.as_view(), name='completar_turno_empleado'),
    path('empleado/turnos/<int:turno_id>/transferir/', TransferirTurnoEmpleadoView.as_view(), name='transferir_turno_empleado'),
    path('turno-actual-empleado/', TurnoActualEmpleadoView.as_view(), name='turno_actual_empleado'),
    path('cola-turnos-empleado/', ListarColaTurnosEmpleadoView.as_view(), name='listar_cola_turnos_empleado'),
    path('estadisticas-empleado/', EstadisticasEmpleadoView.as_view(), name='estadisticas_empleado'),
    path('iniciar-atencion/', IniciarAtencionView.as_view(), name='iniciar_atencion'),
    path('finalizar-atencion/', FinalizarAtencionView.as_view(), name='finalizar_atencion'),
    path('ultimos-turnos-finalizados/', UltimosTurnosFinalizadosView.as_view(), name='ultimos_turnos_finalizados'),
]
