from django import forms
from .models import Stake

class StakeForm(forms.ModelForm):
    class Meta:
        model = Stake
        fields = ('user','marketselection', 'amount',)

