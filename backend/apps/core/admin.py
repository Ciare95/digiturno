from django.contrib import admin
from .models import Sucursal, Servicio


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Sucursal"""
    list_display = ('nombre', 'codigo_sucursal', 'ciudad', 'departamento', 'activa')
    list_filter = ('activa', 'ciudad', 'departamento')
    search_fields = ('nombre', 'codigo_sucursal', 'direccion')
    ordering = ('nombre',)
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'codigo_sucursal', 'direccion', 'telefono')
        }),
        ('Ubicación', {
            'fields': ('ciudad', 'departamento')
        }),
        ('Estado y configuración', {
            'fields': ('activa', 'configuracion')
        }),
    )


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
            'fields': ('tiempo_estimado_atencion', 'color_identificacion', 'icono')
        }),
    )
