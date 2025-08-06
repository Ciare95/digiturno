from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import Empleado
from ..serializers.info_empleado_serializer import InfoEmpleadoSerializer
from ..permissions import EsEmpleado

class InfoEmpleadoView(generics.RetrieveAPIView):
    serializer_class = InfoEmpleadoSerializer
    permission_classes = [IsAuthenticated, EsEmpleado]

    def get_object(self):
        try:
            return Empleado.objects.get(usuario=self.request.user)
        except Empleado.DoesNotExist:
            return None
