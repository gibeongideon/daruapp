from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import C2BTransactionForm
from .models import C2BTransaction
from account.models import CashDeposit
from dashboard.models import WebPa

@login_required(login_url='/users/login')
def mpesa_deposit(request):
    print('mpesa_deposit_TO:', request.user)
    form = C2BTransactionForm()
    if request.method == 'POST':
        data = {}
        data['phone_number'] = request.user.phone_number
        data['amount'] = request.POST.get('amount')
        # form = C2BTransactionForm(data=request.POST)
        form = C2BTransactionForm(data=data)
        if form.is_valid():
            form.save()
            print('YES DONE')

    trans_logz = CashDeposit.objects.filter(user =request.user).order_by('-id')[:10]    
    web_pa , _ = WebPa.objects.get_or_create(id=1)    
    mpesa_header_depo_msg = web_pa.mpesa_header_depo_msg
    
    return render(
        request,
        'cash_trans/mp_deposit.html',
        {'form': form,'trans_logz': trans_logz,
        'mpesa_header_depo_msg': mpesa_header_depo_msg})
