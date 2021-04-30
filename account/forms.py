
from django import forms
from .models import CashWithrawal,RefCreditTransfer

class CashWithrawalForm(forms.ModelForm):
    class Meta:
        model = CashWithrawal
        fields = ('user', 'amount',)

   
class ReferTranferForm(forms.ModelForm):
    class Meta:
        model = RefCreditTransfer
        fields = ('user', 'amount',)     
