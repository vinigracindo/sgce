from django import forms

from sgce.core.models import Event
from sgce.core.widgets import Html5DateInput


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ()
        widgets = {
            'start_date': Html5DateInput(),
            'end_date': Html5DateInput(),
        }