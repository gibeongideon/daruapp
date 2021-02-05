from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import StakeForm,IstakeForm
from .models import Stake, Istake


@login_required(login_url='/user/login')
def daru_spin(request):

    stake_form = StakeForm()
    trans_logz = Stake.objects.filter(
        user=request.user).order_by('-created_at')[:12]

    if request.method == 'POST':

        #is this secure# normal dic generated from imuttable dic//automatic user 
               
        data = {}
        data['user'] = request.user
        data['marketselection'] = request.POST['marketselection']
        data['amount'] = request.POST['amount'] 

        stake_form = StakeForm(data=data)
  
        if stake_form.is_valid():

            stake_form.save()
        else:
            print(stake_form.errors)

    context = {
        'user': request.user, 'stake_form': stake_form,
        'trans_logz': trans_logz
        }

    return render(request, 'daru_wheel/daru_spin.html', context)


@login_required(login_url='/user/login')
def spin(request):

    stake_form = IstakeForm()
    trans_logz = Istake.objects.filter(
        user=request.user).order_by('-created_at')[:12]

    if request.method == 'POST':   
        data = {}
        data['user'] = request.user
        data['marketselection'] = request.POST['marketselection']
        data['amount'] = request.POST['amount'] 

        stake_form = IstakeForm(data=data)
  
        if stake_form.is_valid():

            stake_form.save()
        else:
            print(stake_form.errors)

    context = {
        'user': request.user, 'stake_form': stake_form,
        'trans_logz': trans_logz
        }

    return render(request, 'daru_wheel/ispin.html', context)
