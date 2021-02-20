from django import forms
from .models import Stake, Istake


class StakeForm(forms.ModelForm):
    class Meta:
        model = Stake
        fields = ('user', 'marketselection', 'amount',)


class IstakeForm(forms.ModelForm):
    class Meta:
        model = Istake
        fields = ('user', 'marketselection', 'amount', 'bet_on_real_account')
