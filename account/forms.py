from django import forms
from .models import CashWithrawal, RefCreditTransfer, C2BTransaction, CashTransfer,Checkout
from paypal.pro.forms import PaymentForm


class CashWithrawalForm(forms.ModelForm):
    class Meta:
        model = CashWithrawal
        fields = (
            "user",
            "amount",
        )


class ReferTranferForm(forms.ModelForm):
    class Meta:
        model = RefCreditTransfer
        fields = (
            "user",
            "amount",
        )


class C2BTransactionForm(forms.ModelForm):
    class Meta:
        model = C2BTransaction
        fields = (
            "phone_number",
            "amount",
        )


class CashTransferForm(forms.ModelForm):
    class Meta:
        model = CashTransfer
        fields = (
            "sender",
            "recipient",
            "amount",
        )


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = (
            "user",
            "email",
            "amount",
        )


# class PayPalmentForm(PaymentForm):
#     class Meta:
#         # model = Checkout
#         fields = (
#             "acct",
#             "cvv2",
#         )
