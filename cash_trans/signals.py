from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import C2BTransaction
from mpesa_api.core.models import OnlineCheckoutResponse
from django.contrib.auth import get_user_model
from account.models import (
    current_account_bal_of ,update_account_bal_of, log_record)

User = get_user_model()

#TO REMOVE 4 TEST#RED FLA
@receiver(post_save, sender= C2BTransaction) 
def create_user_account(sender, instance, created, **kwargs):

    try:
        if created:   ##TODO phone NO detection should be flexible enough
            deposited_amount = instance.amount  # NN 

            print(f'phone{str(instance.phone_number)}')  # debug
            
            this_user = User.objects.get(
                phone_number=str(instance.phone_number)) 

            new_bal = current_account_bal_of(this_user.id) + float(deposited_amount)  # F2 # fix unsupported operand type(s) for +: 'float' and 'decimal.Decimal'
            update_account_bal_of(this_user.id, new_bal)  #F3

            log_record(this_user.id, deposited_amount, "mpesa online deposit")
            
    except Exception as e:# implement user wit tat pone does not exist error
        print('MPESA DEPO', e)
