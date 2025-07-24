from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import transaction, models
from django.db.models import Q, Avg, F, Value as V
from django.db.models.functions import Concat
from rest_framework import serializers
import random
import string
import logging

from .models import Turno, CalificacionServicio, ColaTurnos, Notificacion
from .serializers import (
    TurnoSerializer, CrearTurnoSerializer, CalificacionServicioSerializer,
    TransferirTurnoSerializer, ColaTurnosSerializer, EstadisticasEmpleadoSerializer
)
from apps.users.permissions.es_admin import EsEmpleado, EsAdministrador
from apps.users.models.empleado import Empleado
from apps.users.models.usuario import Usuario
from apps.core.models.servicio import Servicio
from apps.core.models.sucursal import Sucursal
from .logic import GestorTurnos