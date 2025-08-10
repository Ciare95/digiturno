from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Empleado, Administrador, EmpleadoServicio


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Configuración del administrador para el modelo Usuario personalizado"""
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información básica', {'fields': ('email',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


class EmpleadoServicioInline(admin.TabularInline):
    model = EmpleadoServicio
    extra = 1

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Empleado"""
    list_display = ('usuario', 'codigo_empleado', 'sucursal', 'ventanilla_asignada', 'estado_conexion')
    inlines = [EmpleadoServicioInline]
    list_filter = ('sucursal', 'estado_conexion')
    search_fields = ('usuario__username', 'usuario__email', 'codigo_empleado')
    raw_id_fields = ('usuario',)
    fieldsets = (
        ('Información básica', {
            'fields': ('usuario', 'codigo_empleado', 'sucursal')
        }),
        ('Asignación', {
            'fields': ('ventanilla_asignada', 'estado_conexion')
        }),
        ('Información adicional', {
            'fields': ('fecha_ingreso', 'configuracion_ui')
        }),
    )
    exclude = ('servicios',)


@admin.register(EmpleadoServicio)
class EmpleadoServicioAdmin(admin.ModelAdmin):
    """Configuración del administrador para asignación de servicios"""
    list_display = ('empleado', 'servicio')
    list_filter = ('servicio',)
    search_fields = ('empleado__codigo_empleado', 'servicio__nombre')

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Administrador"""
    list_display = ('usuario', 'nivel_acceso', 'sucursal')
    list_filter = ('nivel_acceso', 'sucursal')
    search_fields = ('usuario__username', 'usuario__email')
    raw_id_fields = ('usuario',)
    fieldsets = (
        ('Información básica', {
            'fields': ('usuario', 'nivel_acceso', 'sucursal')
        }),
        ('Permisos', {
            'fields': ('permisos',)
        }),
    )
