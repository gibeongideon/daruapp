
from django import forms
from .models import CashWithrawal

class CashWithrawalForm(forms.ModelForm):
    class Meta:
        model = CashWithrawal
        fields = ('user', 'amount',)
