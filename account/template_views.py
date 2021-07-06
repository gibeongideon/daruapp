# from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

# from django.contrib import messages
from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from .forms import CheckoutForm
from paypal.pro.views import PayPalPro
# from paypal.pro.forms import PaymentForm
# from django.forms.utils import ErrorList
# from django.http import HttpResponse
from .models import (
    # TransactionLog,
    RefCredit,
    CashWithrawal,
    Account,
    AccountSetting,
    CashDeposit,
    CashTransfer,
)
from .forms import (
    CashWithrawalForm,
    ReferTranferForm,
    C2BTransactionForm,
    CashTransferForm,
    # PayPalmentForm
)

from dashboard.models import WebPa
from users.models import User


@login_required(login_url="/user/login")
def mpesa_deposit(request):
    print("mpesa_deposit_TO:", request.user)
    form = C2BTransactionForm()
    if request.method == "POST":
        data = {}
        data["phone_number"] = request.user.phone_number
        data["amount"] = request.POST.get("amount")
        # form = C2BTransactionForm(data=request.POST)
        form = C2BTransactionForm(data=data)
        if form.is_valid():
            form.save()
            print("YES DONE")

    trans_logz = CashDeposit.objects.filter(user=request.user).order_by("-id")[:10]
    web_pa, _ = WebPa.objects.get_or_create(id=1)
    mpesa_header_depo_msg = web_pa.mpesa_header_depo_msg

    return render(
        request,
        "account/mp_deposit.html",
        {
            "form": form,
            "trans_logz": trans_logz,
            "mpesa_header_depo_msg": mpesa_header_depo_msg,
        },
    )


# # Use redis cashing here for speed
# @login_required(login_url="/users/login")
# def trans_log(request):
#     trans_logz = TransactionLog.objects.filter(user=request.user)
#     return render(request, "account/trans_log.html", {"trans_logz": trans_logz})


@login_required(login_url="/user/login")
def refer_credit(request):
    form = ReferTranferForm()
    if request.method == "POST":
        data = {}
        data["user"] = request.user
        data["amount"] = request.POST.get("amount")
        form = ReferTranferForm(data=data)
        if form.is_valid():
            form.save()
            print("YES Transer!")

    min_wit, _ = AccountSetting.objects.get_or_create(id=1)
    min_wit = min_wit.min_redeem_refer_credit
    account_bal = float(Account.objects.get(user=request.user).balance)
    refer_bal = float(Account.objects.get(user=request.user).refer_balance)
    refer_credit = RefCredit.objects.filter(user=request.user).order_by("-created_at")
    # if refer_bal<min_wit:
    #     re_to_wit=min_wit-refer_bal
    # elif float(refer_bal)<min_wit:
    #     re_to_wit=0
    # else:
    #     re_to_wit=0

    return render(
        request,
        "account/refer_credit.html",
        {
            "form": form,
            "refer_credit": refer_credit,
            "account_bal": account_bal,
            "refer_bal": refer_bal,
            "min_wit": min_wit,
            # 're_to_wit':re_to_wit
        },
    )


@login_required(login_url="/user/login")
def mpesa_withrawal(request):
    form = CashWithrawalForm()
    if request.method == "POST":
        data = {}
        data["user"] = request.user
        data["amount"] = request.POST.get("amount")
        form = CashWithrawalForm(data=data)
        if form.is_valid():
            form.save()
            print("YES DONECW!")

    trans_logz = CashWithrawal.objects.filter(user=request.user).order_by("-id")[:10]

    return render(
        request,
        "account/mpesa_withrawal.html",
        {"form": form, "trans_logz": trans_logz},
    )


@login_required(login_url="/user/login")
def cash_trans(request):
    form = CashTransferForm()
    if request.method == "POST":
        data = {}
        data["sender"] = request.user
        recipient = request.POST.get("recipient")

        try:
            recipient = User.objects.get(username=recipient.strip())
        except Exception:
            pass

        data["recipient"] = recipient
        data["amount"] = request.POST.get("amount")
        form = CashTransferForm(data=data)
        if form.is_valid():
            form.save()
        if form.errors:
            print(form.errors)

    trans_logz = CashTransfer.objects.filter(sender=request.user).order_by("-id")[:10]

    return render(
        request, "account/cash_trans.html", {"form": form, "trans_logz": trans_logz}
    )



from django.views.generic import FormView
from django.views.generic import TemplateView
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm


class PaypalFormView(FormView):
    template_name = 'paypal_form.html'
    form_class = PayPalPaymentsForm

    def get_initial(self):
        return {
            "cmd": "_xclick-subscriptions",
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": 20,
            "currency_code": "USD",
            "item_name": 'Example item',
            "invoice": 1234,
            "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
            # "return_url": self.request.build_absolute_uri(reverse('paypal-return')),
            # "cancel_return": self.request.build_absolute_uri(reverse('paypal-cancel')),
            "lc": 'EN',
            "no_shipping": '1',
            
        }
        


class PaypalReturnView(TemplateView):
    template_name = 'paypal_success.html'


class PaypalCancelView(TemplateView):
    template_name = 'paypal_cancel.html'


def nvp_handler(nvp):
    # This is passed a PayPalNVP object when payment succeeds.
    # This should do something useful!
    print('nvp-NVP')
    print(nvp)    
    pass


@login_required(login_url="/user/login")
def paypal_topup(request):
    item = {"amt": "5.00",  # amount to charge for item
            "inv": f"darispin-{request.user.id} ",      # unique tracking variable paypal
            "custom": f"{request.user.id}",       # custom tracking variable for you
            "cancelurl": "http://darispin.ga/deposit_withraw",  # Express checkout cancel url
            "returnurl": "http://darispin.ga/"}  # Express checkout return url

    ppp = PayPalPro(
              item=item,
            #   payment_form_cls=PayPalmentForm,                      # what you're selling
              payment_template="payment.html",      # template name for payment
              confirm_template="confirmation.html", # template name for confirmation
              success_url="/",              # redirect location after success
              nvp_handler=nvp_handler)
    return ppp(request)
