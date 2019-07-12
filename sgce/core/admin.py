from django.contrib import admin
from sgce.core.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'created_by')
    search_fields  = ['name', 'created_by']
    date_hierarchy = 'created_at'
