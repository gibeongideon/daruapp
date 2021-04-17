from django import forms
from .models import C2BTransaction

class C2BTransactionForm(forms.ModelForm):
    class Meta:
        model = C2BTransaction
        fields = ('phone_number', 'amount',)

