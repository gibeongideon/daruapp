
from django import forms
from .models import CashWithrawal,RefCreditTransfer,C2BTransaction,TransferCash

class CashWithrawalForm(forms.ModelForm):
    class Meta:
        model = CashWithrawal
        fields = ('user', 'amount',)

   
class ReferTranferForm(forms.ModelForm):
    class Meta:
        model = RefCreditTransfer
        fields = ('user', 'amount',)     
        

class C2BTransactionForm(forms.ModelForm):
    class Meta:
        model = C2BTransaction
        fields = ('phone_number', 'amount',)
        
class TransferCashForm(forms.ModelForm):
    class Meta:
        model = TransferCash
        fields = ('user_from','user_to', 'amount',)