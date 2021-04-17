from django.db import models
from mpesa_api.core.mpesa import Mpesa
from account.models import TimeStamp

class C2BTransaction(TimeStamp):
    phone_number = models.BigIntegerField()
    amount       = models.DecimalField(max_digits=20, decimal_places=2)
    success      = models.BooleanField(default=False, blank=True,null=True)

    def save(self, *args, **kwargs):
        try:
            Mpesa.stk_push(
                self.phone_number,
                self.amount,
                account_reference=f'Pay Daru Casino :{self.amount}',
                is_paybill=True)

            self. success = True
            
        except Exception as tx:
            print(f'C2BTransaction:{tx}')
            return
        super().save(*args, **kwargs)


## IDEA

# Account be updated based on successfull Responce# Not sucess of tis
     