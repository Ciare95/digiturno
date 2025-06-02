from rest_framework import serializers
from .models import Sucursal, Servicio, Configuracion


class SucursalSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Sucursal"""
    
    class Meta:
        model = Sucursal
        fields = [
            'id', 'nombre', 'codigo_sucursal', 'direccion', 
            'telefono', 'ciudad', 'departamento', 'activa'
        ]


class ServicioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Servicio"""
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    
    class Meta:
        model = Servicio
        fields = [
            'id', 'nombre', 'codigo_servicio', 'sucursal', 
            'sucursal_nombre', 'tiempo_estimado_atencion',
            'color_identificacion', 'icono'
        ]


class ConfiguracionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Configuracion"""
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    
    class Meta:
        model = Configuracion
        fields = [
            'id', 'clave', 'valor', 'descripcion', 'categoria',
            'es_global', 'sucursal', 'sucursal_nombre',
            'fecha_creacion', 'fecha_actualizacion'
        ]
