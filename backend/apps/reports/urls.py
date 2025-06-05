from django.urls import path
from .views import ReporteAvanzadoView

urlpatterns = [
    path('admin/reportes/', ReporteAvanzadoView.as_view(), name='reportes_avanzados'),
]