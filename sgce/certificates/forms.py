from io import StringIO

from django import forms
from django.core.validators import FileExtensionValidator
from django_select2.forms import Select2Widget

import csv

from sgce.certificates.models import Template, Certificate, Participant
from sgce.core.models import Event


class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        exclude = ('created_by',)


class TemplateDuplicateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ('event',)
        help_texts = {
            'event': ('Escolha o evento que você quer aplicar este modelo'),
        }

    def __init__(self, user, *args, **kwargs):
        super(TemplateDuplicateForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['event'].queryset = Event.objects.filter(created_by=user)


class CertificatesCreatorForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ('template', )
        widgets = {
            'template': Select2Widget,
        }

    def __init__(self, user, *args, **kwargs):
        super(CertificatesCreatorForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['template'].queryset = Template.objects.filter(event__created_by=user)


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        exclude = ()
