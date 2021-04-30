from django.dispatch import receiver
from django.db.models.signals import post_save
# from  users.models import User
from .models import Account
from mpesa_api.core.models import OnlineCheckoutResponse
from .models import (
    Account,CashWithrawal, CashDeposit,
    update_account_bal_of, current_account_bal_of, log_record
    )
from django.contrib.auth import get_user_model
from daru_wheel.models import Stake # DD

User = get_user_model()


@receiver(post_save, sender=User) 
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.update_or_create(user=instance)
        # print(f'User{instance.username} Account Created ')#Debug



@receiver(post_save, sender= OnlineCheckoutResponse) #TODO
def update_account_balance_on_mpesa_deposit(sender, instance, created, **kwargs):
    # if created:
    try:
        try:
            this_user = User.objects.get(
                phone_number=str(instance.phone)
                )
        except :
            print(f'user of {str(instance.phone)} does not Exist')#onlyinpaybill/notTiz
            this_user = User.objects.create_user(username=str(instance.phone),password=str(instance.phone))#3#??   


        if int(instance.result_code) == 0:                         
            CashDeposit.objects.create(
                user=this_user,
                amount=instance.amount,
                deposit_type='M-pesa Deposit',
                confirmed=True
                ) 
        else:        
            CashDeposit.objects.create(
                user=this_user,
                amount=instance.amount,
                deposit_type='M-pesa Deposit',
                confirmed=False
                )         

            # new_bal = current_current_account_bal_ofaccount_bal_of(this_user) + float(deposited_amount)  # F2 # fix unsupported operand type(s) for +: 'float' and 'decimal.Decimal'
            # update_account_bal_of(this_user, new_bal)  #F3
            # log_record(this_user.id, deposited_amount, "mpesa online deposit")
            
    except Exception as e:
        print('MPESA DEPO',e)


@receiver(post_save, sender=Stake) 
def update_user_withraw_power_onstake(sender, instance, created, **kwargs):
    try:        
        if created and instance.bet_on_real_account is True:
            now_withrawable = float(Account.objects.get(user_id =instance.user_id).withraw_power)
            # print(f'now_withrawableS:{now_withrawable}')
            added_amount = float(instance.amount)
            # print(f'added_amountS:{added_amount}')
            total_withwawable = now_withrawable + added_amount

            if total_withwawable > 0:
                Account.objects.filter(user_id=instance.user_id).update(withraw_power=total_withwawable)

    except Exception as e:
        print('Withrable cal err_onstake', e)


# @receiver(post_save, sender=CashWithrawal)
# def update_user_withraw_power_onwithraw(sender, instance, created, **kwargs):
#     try:
#         if created and instance.withrawned is True:  # and instance.active=False:
      
#             now_withrawable = float(Account.objects.get(user_id=instance.user_id).withraw_power)
#             print(f'now_withrawableW:{now_withrawable}')
#             deduct_amount = float(instance.amount)
#             print(f'added_amountW:{deduct_amount}')
#             total_withwawable = now_withrawable - deduct_amount

#             if total_withwawable > 0:
#                 Account.objects.filter(user_id =instance.user_id).update(withraw_power= total_withwawable)

#     except Exception as e:
#         print('Withrable cal err_onwithraw',e)

