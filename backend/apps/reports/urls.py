from django.urls import path
from .views import DashboardAdminView, ReporteAvanzadoView

urlpatterns = [
    path('admin/panel/', DashboardAdminView.as_view(), name='dashboard_admin'),
    path('admin/reportes/', ReporteAvanzadoView.as_view(), name='reportes_avanzados'),
]