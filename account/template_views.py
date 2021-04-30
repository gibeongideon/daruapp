
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms.utils import ErrorList
from django.http import HttpResponse

from .models import TransactionLog, RefCredit, CashWithrawal ,Account ,AccountSetting
from .forms import CashWithrawalForm


# Use redis cashing here for speed
@login_required(login_url='/users/login')
def trans_log(request):
    trans_logz =TransactionLog.objects.filter(user =request.user)
    
    return render(request, 'account/trans_log.html',{'trans_logz': trans_logz})

@login_required(login_url='/users/login')
def refer_credit(request):
    min_wit = AccountSetting.objects.get(id=1).min_redeem_refer_credit
    refer_bal = Account.objects.get(user=request.user).refer_balance
    refer_credit = RefCredit.objects.filter(user =request.user).order_by('-created_at')
    
    return render(request, 'account/refer_credit.html',{'refer_credit': refer_credit,'refer_bal': refer_bal,'min_wit': min_wit})





@login_required(login_url='/users/login')
def mpesa_withrawal(request):
    form = CashWithrawalForm()
    if request.method == 'POST':
        data = {}
        data['user'] = request.user
        data['amount'] = request.POST.get('amount')
        form = CashWithrawalForm(data=data)
        if form.is_valid():
            form.save()
            print('YES DONECW!')
        else:
            print('ERRRRR', form.errors)
    trans_logz = CashWithrawal.objects.filter(user =request.user).order_by('-id')[:10]        

    return render(request, 'account/mpesa_withrawal.html',{'form': form,'trans_logz': trans_logz})