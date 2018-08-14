from django import forms
from sgce.core.models import Event
from sgce.core.widgets import Html5DateInput


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('created_by',)
        widgets = {
            'start_date': Html5DateInput(format='%Y-%m-%d'),
            'end_date': Html5DateInput(format='%Y-%m-%d'),
        }


class HomeForm(forms.Form):
    cpf = forms.CharField(
        max_length=14,
        label='CPF',
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu CPF para buscar seus Certificados',
                                      'data-mask': '000.000.000-00'}),
    )