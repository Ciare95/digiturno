from django.urls import path
from .views import ReporteAvanzadoView

urlpatterns = [
    path('reportes/', ReporteAvanzadoView.as_view(), name='reportes_avanzados'),
]