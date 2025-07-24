from django.contrib import admin
from .models import Sucursal, Servicio, Configuracion, DiaSucursal
from django.db.models import Count


class ConfiguracionInline(admin.TabularInline):
    model = Configuracion
    extra = 1


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Sucursal"""
    inlines = [ConfiguracionInline]
    list_display = ('nombre', 'codigo_sucursal', 'ciudad', 'total_servicios', 'activa')
    list_filter = ('activa', 'ciudad', 'departamento')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            total_servicios=Count('servicio')
        )

    def total_servicios(self, obj):
        return obj.total_servicios
    total_servicios.short_description = "Total Servicios"


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Servicio"""
    list_display = ('nombre', 'codigo_servicio', 'sucursal', 'tiempo_estimado_atencion')
    list_filter = ('sucursal',)
    search_fields = ('nombre', 'codigo_servicio')
    ordering = ('sucursal', 'nombre')
    fieldsets = (
        ('Información del servicio', {
            'fields': ('nombre', 'codigo_servicio', 'sucursal')
        }),
        ('Configuración', {
            'fields': ('tiempo_estimado_atencion', )
        }),
    )


@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Configuracion"""
    list_display = ('clave', 'valor', 'categoria', 'sucursal', 'fecha_actualizacion')
    list_filter = ('categoria', 'sucursal')
    search_fields = ('clave', 'descripcion')
    list_editable = ('valor',)

    fieldsets = (
        ('Información básica', {
            'fields': ('clave', 'valor', 'descripcion')
        }),
        ('Configuración', {
            'fields': ('categoria', 'sucursal', 'es_global')
        }),
    )

@admin.register(DiaSucursal)
class DiaSucursalAdmin(admin.ModelAdmin):
    list_display = ('sucursal', 'dia_semana', 'hora_apertura', 'hora_cierre', 'activo')
    list_filter = ('sucursal', 'dia_semana')
    search_fields = ('sucursal__nombre', 'dia_semana__nombre')
    ordering = ('sucursal', 'dia_semana')