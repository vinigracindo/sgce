from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'is_superuser', 'username', 'password', 'groups']
        widgets = {
            'password': forms.PasswordInput,
            'groups': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True


class UserUpdateForm(UserForm):
    class Meta(UserForm.Meta):
        exclude = ('password',)


class ProfileUpdateForm(UserForm):
    class Meta(UserForm.Meta):
        exclude = ('is_superuser', 'groups')

    def clean_password(self):
        password = make_password(self.cleaned_data['password'])
        return password
