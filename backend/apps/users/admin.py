from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Empleado, Administrador, UsuarioSinStaff


@admin.register(UsuarioSinStaff)
class UsuarioSinStaffAdmin(admin.ModelAdmin):
    """Configuración simplificada para usuarios sin autenticación"""
    list_display = ('cedula', 'telefono', 'email')
    search_fields = ('cedula', 'telefono', 'email')
    fields = ('cedula', 'telefono', 'email')


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
