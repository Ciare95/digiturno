from rest_framework import serializers
from apps.core.models.servicio import Servicio

class TransferirTurnoSerializer(serializers.Serializer):
    """Serializador para la transferencia de turnos por un empleado."""
    nuevo_servicio_id = serializers.IntegerField(required=True, help_text="ID del nuevo servicio al que se transferirá el turno.")

    def validate_nuevo_servicio_id(self, value):
        """Verifica que el nuevo_servicio_id corresponda a un servicio válido y activo."""
        # Esta validación asume que el servicio existe y está activo.
        # La validación de que el servicio pertenece a la sucursal del empleado
        # se maneja directamente en la vista, ya que el serializer no tiene acceso directo al request.user aquí.
        if not Servicio.objects.filter(id=value, activo=True).exists():
            raise serializers.ValidationError("El servicio especificado no existe o no está activo.")
        return value