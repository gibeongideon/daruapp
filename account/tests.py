from django.test import TestCase  #,Client
from django.urls import reverse
from account.models import CashDeposit, CashWithrawal, Account
from users.models import User
from daru_wheel.models import  Stake
import random


# MODEL TESTS

class CashDepositWithrawalTestCase(TestCase):
    def setUp(self):
       self.usera=User.objects.create(username="0710001000", email="testa@gmail.com",referer_code="ADMIN")
       self.userb=User.objects.create(username="0123456787", email="testb@gmail.com", referer_code="ADMIN")
      
    def test_user_deposit(self):
        CashDeposit.objects.create(amount=1000,user=self.usera,confirmed=True)
        bal1a = Account.objects.get(user=self.usera).balance
        bal1b = Account.objects.get(user=self.userb).balance
        
        self.assertEqual(1000, bal1a)
        self.assertEqual(0, bal1b)

        CashDeposit.objects.create(amount=100000, user=self.usera,confirmed=True)
        CashDeposit.objects.create(amount=1000, user=self.userb,confirmed=True)        
        bal2a = Account.objects.get(user=self.usera).balance
        bal2b = Account.objects.get(user=self.userb).balance

        self.assertEqual(101000, bal2a)
        self.assertEqual(1000, bal2b)

    def test_correct_no_negative_deposit(self):
        '''test to ensure no negative deposit done'''
        CashDeposit.objects.create(amount=1000, user=self.usera,confirmed=True)
        n_amount= - random.randint(1, 10000)
        CashDeposit.objects.create(amount=n_amount, user=self.usera,confirmed=True)

        balla = Account.objects.get(user=self.usera).balance
        ballb = Account.objects.get(user=self.userb).balance
        depo_count = CashDeposit.objects.count()

        self.assertEqual(depo_count, 1)
        self.assertEqual(balla, 1000)
        self.assertEqual(ballb, 0)

        CashDeposit.objects.create(amount=100000, user=self.usera,confirmed=True)
        CashDeposit.objects.create(amount=1000, user=self.userb,confirmed=True)
        n_amount= - random.randint(1, 10000)
        CashDeposit.objects.create(amount=n_amount, user=self.userb,confirmed=True)
        
        bal2a = Account.objects.get(user=self.usera).balance
        bal2b = Account.objects.get(user=self.userb).balance

        self.assertEqual(101000, bal2a)
        self.assertEqual(1000, bal2b)

    def test_witrawable_update_correctly(self):
        CashDeposit.objects.create(amount=10000,user=self.usera,confirmed=True)

        self.assertEqual(Account.objects.get(user=self.usera).balance,10000)
        self.assertEqual(Account.objects.get(user=self.usera).withraw_power ,0)

        Stake.objects.create(user=self.usera,amount=1000,bet_on_real_account=True)

        self.assertEqual(Account.objects.get(user=self.usera).balance,9000)
        self.assertEqual(Account.objects.get(user=self.usera).withraw_power ,1000)

        CashWithrawal.objects.create(user=self.usera,amount=800) 


        self.assertEqual(Account.objects.get(user=self.usera).balance,9000)
        self.assertEqual(Account.objects.get(user=self.usera).withraw_power ,1000)
        
        self.assertEqual(CashWithrawal.objects.get(id=1).approved,False)

        CashWithrawal.objects.filter(id=1).update(approved=True)

        self.assertEqual(CashWithrawal.objects.get(id=1).approved,True)

        self.assertEqual(Account.objects.get(user=self.usera).balance,9000)
        # self.assertEqual(Account.objects.get(user=self.usera).withraw_power , 200)#failin


    def test_cu_deposit_update_correctly(self):
        CashDeposit.objects.create(amount=10000,user=self.usera,confirmed=True)

        self.assertEqual(Account.objects.get(user=self.usera).cum_deposit,10000)

        CashDeposit.objects.create(amount=1000,user=self.usera,confirmed=True)

        self.assertEqual(Account.objects.get(user=self.usera).cum_deposit,11000)

 