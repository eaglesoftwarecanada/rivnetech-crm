from django.contrib import admin
from .models import HealthDatabase


@admin.register(HealthDatabase)
class HealthDatabaseAdmin(admin.ModelAdmin):
    list_display = ("alias", "type", "host", "port", "is_enabled", "updated_at")
    list_filter = ("type", "is_enabled")
    search_fields = ("alias", "name", "host")
