from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

# from django.contrib import messages
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from decimal import Decimal
# from paypal.standard.forms import PayPalPaymentsForm
# from .forms  import CheckoutForm

from paypal.pro.views import PayPalPro
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

        print("USSER_T", recipient)

        data["recipient"] = recipient
        data["amount"] = request.POST.get("amount")
        form = CashTransferForm(data=data)
        if form.is_valid():
            form.save()
            print("YES DONE_TRANSFER!")
        if form.errors:
            print(form.errors)

    trans_logz = CashTransfer.objects.filter(sender=request.user).order_by("-id")[:10]

    return render(
        request, "account/cash_trans.html", {"form": form, "trans_logz": trans_logz}
    )




# def checkout(request):
#     if request.method == 'POST':
#         form = CheckoutForm(request.POST)
#         if form.is_valid():
#             return redirect('process_payment')

#     else:
#         form = CheckoutForm()
#         return render(request, 'account/paypal/checkout.html', locals())


# def process_payment(request):
#     host = request.get_host()

#     paypal_dict = {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': 50,
#         'item_name': 'dspay',
#         'invoice': '',
#         'currency_code': 'USD',
#         'notify_url': 'http://{}{}'.format(host,
#                                            reverse('paypal-ipn')),
#         'return_url': 'http://{}{}'.format(host,
#                                            reverse('payment_done')),
#         'cancel_return': 'http://{}{}'.format(host,
#                                               reverse('payment_cancelled')),
#     }

#     form = PayPalPaymentsForm(initial=paypal_dict)
#     return render(request, 'account/paypal/process_payment.html', {'form': form})


# @csrf_exempt
# def payment_done(request):
#     return render(request, 'account/paypal/payment_done.html')


# @csrf_exempt
# def payment(request):
#     return render(request, 'account/paypal/payment_cancelled.html')


def nvp_handler(nvp):
    # This is passed a PayPalNVP object when payment succeeds.
    # This should do something useful!
    print(nvp)
    pass


@login_required(login_url="/user/login")
def account_topup(request):
    item = {"paymentrequest_0_amt": "10.00",  # amount to charge for item
            "inv": "inventory",         # unique tracking variable paypal
            "custom": "tracking",       # custom tracking variable for you
            "cancelurl": "http://...",  # Express checkout cancel url
            "returnurl": "http://..."}  # Express checkout return url

    ppp = PayPalPro(
              item=item,                            # what you're selling
              payment_template="payment.html",      # template name for payment
              confirm_template="confirmation.html", # template name for confirmation
              success_url="/success/",              # redirect location after success
              nvp_handler=nvp_handler)
    return ppp(request)