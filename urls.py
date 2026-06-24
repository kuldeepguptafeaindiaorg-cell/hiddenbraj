from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # ── Main website ────────────────────────────────────────────────────────
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # ── REST API ─────────────────────────────────────────────────────────────
    path('api/register',               views.RegisterView.as_view(),              name='api-register'),
    path('yatra-stats',                views.StatsView.as_view(),                 name='api-stats'),
    path('api/admin-registrations',    views.AdminRegistrationsView.as_view(),    name='api-admin-registrations'),
    path('api/admin-export-csv',       views.AdminExportCSVView.as_view(),        name='api-admin-export-csv'),

    # ── Admin panel ──────────────────────────────────────────────────────────
    path('admin/', views.AdminPanelView.as_view(), name='admin-panel'),
]
