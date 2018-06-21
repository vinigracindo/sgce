from django import forms
from django.core.exceptions import SuspiciousOperation

from sgce.core.models import Event
from sgce.core.widgets import Html5DateInput


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('created_by',)
        widgets = {
            'start_date': Html5DateInput(),
            'end_date': Html5DateInput(),
        }