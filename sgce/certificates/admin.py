from django.contrib import admin
from sgce.certificates.models import Template, Certificate, Participant, CertificateHistory


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'event', 'created_at')
    search_fields = ['__str__']
    date_hierarchy = 'created_at'


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('dni', 'name', 'email')
    search_fields = ['dni', 'name']


admin.site.register(Certificate)
admin.site.register(CertificateHistory)
