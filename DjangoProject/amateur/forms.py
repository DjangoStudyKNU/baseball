from django import forms
from amateur.models import Player

class SignForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['email', ]

