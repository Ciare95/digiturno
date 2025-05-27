from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Empleado, Administrador


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Configuración del administrador para el modelo Usuario personalizado"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'telefono', 'cedula', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cedula')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'telefono', 'cedula')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined', 'ultimo_acceso')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'telefono', 'cedula'),
        }),
    )


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Empleado"""
    list_display = ('usuario', 'codigo_empleado', 'sucursal', 'ventanilla_asignada', 'estado_conexion')
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
