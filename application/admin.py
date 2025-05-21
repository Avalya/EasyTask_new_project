from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'app_type', 'status',
        'department', 'assigned_to', 'submitted_at'
    )
    list_filter = ('status', 'department', 'app_type')
    search_fields = ('full_name', 'phone', 'reg_number')
    list_editable = ('status', 'department', 'assigned_to')
    ordering = ('-submitted_at',)
