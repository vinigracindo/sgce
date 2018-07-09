from django import forms

from sgce.certificates.models import Template


class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        exclude = ('created_by',)