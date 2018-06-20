from django import forms


class Html5DateInput(forms.DateInput):
    input_type = 'date'