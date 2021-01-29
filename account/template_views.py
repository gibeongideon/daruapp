
from django.shortcuts import render, redirect ,reverse
from django.contrib.auth.decorators import login_required
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .models import TransactionLog,RefCredit


# Use redis cashing here for speed
@login_required(login_url='/users/login')
def trans_log(request):
    trans_logz =TransactionLog.objects.filter(user =request.user)
    
    return render(request, 'account/trans_log.html',{'trans_logz': trans_logz})

@login_required(login_url='/users/login')
def refer_credit(request):
    refer_credit = RefCredit.objects.filter(user =request.user)
    
    return render(request, 'account/refer_credit.html',{'refer_credit': refer_credit})
