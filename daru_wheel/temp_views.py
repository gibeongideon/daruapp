from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import StakeForm,IstakeForm
from .models import Stake, WheelSpin


# @login_required(login_url='/user/login')
# def daru_spin(request):

#     stake_form = StakeForm()
#     trans_logz = Stake.objects.filter(
#         user=request.user).order_by('-created_at')[:12]

#     if request.method == 'POST':
     
#         data = {}
#         data['user'] = request.user
#         data['marketselection'] = request.POST.get('marketselection')
#         data['amount'] = request.POST.get('amount')
        
#         stake_form = StakeForm(data=data)
  
#         if stake_form.is_valid():

#             stake_form.save()
#         else:
#             print(stake_form.errors)

#     context = {
#         'user': request.user, 'stake_form': stake_form,
#         'trans_logz': trans_logz
#         }

#     return render(request, 'daru_wheel/daru_spin.html', context)

@login_required(login_url='/user/login')
def spin(request):

    stake_form = IstakeForm()
    trans_logz = Stake.objects.filter(
        user=request.user,market=None,has_market=False).order_by('-created_at')[:12]

    if request.method == 'POST':  
        print('YOYOYO') 
        data = {}
        data['user'] = request.user
        data['marketselection'] = request.POST.get('marketselection')
        data['amount'] = request.POST.get('amount')
        data['bet_on_real_account'] = request.POST.get("bet_on_real_account")

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




@login_required(login_url='/user/login')
def daru_spin(request):
    try:
        market_id = max((obj.id for obj in WheelSpin.objects.all()))
        this_wheelspin = WheelSpin.objects.get(id =market_id )
    except Exception as mae:
        this_wheelspin,_ = WheelSpin.objects.get_or_create(id =1)
        pass       
   
    stake_form = StakeForm()
    trans_logz = Stake.objects.filter(
        user=request.user,has_market=True).order_by('-created_at')[:12]

    if request.method == 'POST':
        # if this_wheelspin.place_stake_is_active:# 
        market = this_wheelspin
        print('ID31')
        print(market.id)
        print('ID31')
    
        data = {}
        data['user'] = request.user
        data['market'] = market
        data['marketselection'] = request.POST.get('marketselection')
        data['amount'] = request.POST.get('amount')
    
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