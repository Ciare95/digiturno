from django.contrib import admin
from .models import Turno, CalificacionServicio, ColaTurnos, Notificacion, EstadisticaEmpleado


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Turno"""
    list_display = ('numero_turno', 'servicio', 'sucursal', 'estado', 'fecha_creacion', 'empleado')
    list_filter = ('estado', 'servicio', 'sucursal', 'es_agendado')
    search_fields = ('numero_turno', 'observaciones')
    date_hierarchy = 'fecha_creacion'
    ordering = ('-fecha_creacion',)
    fieldsets = (
        ('Información básica', {
            'fields': ('numero_turno', 'servicio', 'sucursal', 'usuario')
        }),
        ('Estado', {
            'fields': ('estado', 'prioridad', 'empleado')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_llamado', 'fecha_inicio_atencion', 'fecha_finalizacion')
        }),
        ('Agendamiento', {
            'fields': ('es_agendado', 'fecha_agendada', 'tiempo_espera_estimado')
        }),
        ('Notas', {
            'fields': ('observaciones',)
        }),
    )
    readonly_fields = ('fecha_creacion',)


@admin.register(CalificacionServicio)
class CalificacionServicioAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo CalificacionServicio"""
    list_display = ('turno', 'calificacion', 'servicio', 'empleado', 'fecha_calificacion')
    list_filter = ('calificacion', 'servicio', 'fecha_calificacion')
    search_fields = ('comentario', 'turno__numero_turno')
    date_hierarchy = 'fecha_calificacion'
    ordering = ('-fecha_calificacion',)
    fieldsets = (
        ('Relaciones', {
            'fields': ('turno', 'usuario', 'empleado', 'servicio')
        }),
        ('Evaluación', {
            'fields': ('calificacion', 'comentario', 'aspectos_evaluados')
        }),
        ('Fechas', {
            'fields': ('fecha_calificacion',)
        }),
    )
    readonly_fields = ('fecha_calificacion',)


@admin.register(ColaTurnos)
class ColaTurnosAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo ColaTurnos"""
    list_display = ('turno', 'servicio', 'posicion_cola', 'fecha_ingreso_cola', 'activo')
    list_filter = ('servicio', 'activo')
    search_fields = ('turno__numero_turno',)
    date_hierarchy = 'fecha_ingreso_cola'
    ordering = ('posicion_cola',)
    fieldsets = (
        ('Información básica', {
            'fields': ('turno', 'servicio', 'posicion_cola')
        }),
        ('Estado', {
            'fields': ('activo', 'tiempo_espera_estimado')
        }),
        ('Fechas', {
            'fields': ('fecha_ingreso_cola',)
        }),
    )
    readonly_fields = ('fecha_ingreso_cola',)


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Notificacion"""
    list_display = ('titulo', 'tipo', 'usuario', 'turno', 'leida', 'fecha_envio')
    list_filter = ('tipo', 'leida', 'canal')
    search_fields = ('titulo', 'mensaje', 'usuario__username')
    date_hierarchy = 'fecha_envio'
    ordering = ('-fecha_envio',)
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'mensaje', 'tipo')
        }),
        ('Destinatario', {
            'fields': ('usuario', 'turno')
        }),
        ('Estado', {
            'fields': ('leida', 'canal', 'fecha_lectura')
        }),
        ('Fechas', {
            'fields': ('fecha_envio',)
        }),
    )
    readonly_fields = ('fecha_envio',)


@admin.register(EstadisticaEmpleado)
class EstadisticaEmpleadoAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo EstadisticaEmpleado"""
    list_display = ('empleado', 'fecha', 'turnos_atendidos', 'tiempo_promedio_atencion', 'calificacion_promedio')
    list_filter = ('fecha',)
    search_fields = ('empleado__usuario__username', 'empleado__codigo_empleado')
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)
    fieldsets = (
        ('Información básica', {
            'fields': ('empleado', 'fecha')
        }),
        ('Estadísticas de turnos', {
            'fields': ('turnos_atendidos', 'turnos_transferidos')
        }),
        ('Estadísticas de tiempo', {
            'fields': ('tiempo_promedio_atencion', 'tiempo_conectado')
        }),
        ('Calificación', {
            'fields': ('calificacion_promedio',)
        }),
    )
