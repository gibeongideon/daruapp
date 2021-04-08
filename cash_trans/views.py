from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import C2BTransactionForm
from .models import C2BTransaction

@login_required(login_url='/users/login')
def mpesa_deposit(request):
    print(request.user)
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
        else:
            print('ERRRRR', form.errors)
    # trans_logz = CashDeposit.objects.filter(user =request.user).order_by('-id')[:10]        
    return render(request, 'cash_trans/mp_deposit.html', {'form': form})
