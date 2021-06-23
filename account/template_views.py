from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

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


@login_required(login_url="/users/login")
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


@login_required(login_url="/users/login")
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


@login_required(login_url="/users/login")
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


@login_required(login_url="/users/login")
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
