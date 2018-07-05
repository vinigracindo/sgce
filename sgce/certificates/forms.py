from django import forms

from sgce.certificates.models import Template
from sgce.core.widgets import Html5DateInput


class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        exclude = ('created_by',)