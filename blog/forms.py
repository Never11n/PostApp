from django import forms
from .models import User
from secrets import compare_digest


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if not compare_digest(password, password_confirm):
            raise forms.ValidationError("Passwords do not match")
