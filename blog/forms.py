from django import forms
from ..API.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
