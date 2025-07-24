from rest_framework import serializers
from ..models import DiasSemana

class DiasSemanaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo DiasSemana"""
    class Meta:
        model = DiasSemana
        fields = ['id', 'nombre']
        read_only_fields = ['id']
