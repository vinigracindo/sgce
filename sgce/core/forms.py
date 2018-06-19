from django import forms
from sgce.core.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ()