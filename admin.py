from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'city', 'tour_type', 'created_at']
    list_filter  = ['tour_type', 'created_at']
    search_fields = ['name', 'phone', 'email', 'city']
    readonly_fields = ['created_at', 'ip_address']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
