from django.contrib import admin
from sgce.certificates.models import Template, Certificate, Participant, CertificateHistory


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'event', 'created_at')
    search_fields  = ['__str__']
    date_hierarchy = 'created_at'


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'name', 'email')
    search_fields  = ['cpf', 'name']


admin.site.register(Certificate)
admin.site.register(CertificateHistory)