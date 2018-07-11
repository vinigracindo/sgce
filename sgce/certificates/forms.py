from django import forms

from sgce.certificates.models import Template
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