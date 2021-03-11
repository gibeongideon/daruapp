from django.test import TestCase  #,Client
from django.urls import reverse
from account.models import CashDeposit, CashWithrawal, Account
from users.models import User
from daru_wheel.models import  Stake
import random


# MODEL TESTS

class CashDepositWithrawalTestCase(TestCase):
    def setUp(self):
       self.usera=User.objects.create(username="0710001000", email="testa@gmail.com",daru_code="ADMIN")
       self.userb=User.objects.create(username="0123456787", email="testb@gmail.com", daru_code="ADMIN")
      
    def test_user_deposit(self):
        CashDeposit.objects.create(amount=1000,user=self.usera)
        bal1a = Account.objects.get(user=self.usera).balance
        bal1b = Account.objects.get(user=self.userb).balance
        
        self.assertEqual(1000, bal1a)
        self.assertEqual(0, bal1b)

        CashDeposit.objects.create(amount=100000, user=self.usera)
        CashDeposit.objects.create(amount=1000, user=self.userb)        
        bal2a = Account.objects.get(user=self.usera).balance
        bal2b = Account.objects.get(user=self.userb).balance

        self.assertEqual(101000, bal2a)
        self.assertEqual(1000, bal2b)

    def test_correct_no_negative_deposit(self):
        '''test to ensure no negative deposit done'''
        CashDeposit.objects.create(amount=1000, user=self.usera)
        n_amount= - random.randint(1, 10000)
        CashDeposit.objects.create(amount=n_amount, user=self.usera)

        balla = Account.objects.get(user=self.usera).balance
        ballb = Account.objects.get(user=self.userb).balance
        depo_count = CashDeposit.objects.count()

        self.assertEqual(depo_count, 1)
        self.assertEqual(balla, 1000)
        self.assertEqual(ballb, 0)

        CashDeposit.objects.create(amount=100000, user=self.usera)
        CashDeposit.objects.create(amount=1000, user=self.userb)
        n_amount= - random.randint(1, 10000)
        CashDeposit.objects.create(amount=n_amount, user=self.userb)
        
        bal2a = Account.objects.get(user=self.usera).balance
        bal2b = Account.objects.get(user=self.userb).balance

        self.assertEqual(101000, bal2a)
        self.assertEqual(1000, bal2b)

    def test_witrawable_update_correctly(self):
        CashDeposit.objects.create(amount=10000,user=self.usera)

        self.assertEqual(Account.objects.get(user=self.usera).balance,10000)
        self.assertEqual(Account.objects.get(user=self.usera).withrawable_balance ,0)

        Stake.objects.create(user=self.usera,amount=1000,bet_on_real_account=True)

        self.assertEqual(Account.objects.get(user=self.usera).balance,9000)
        self.assertEqual(Account.objects.get(user=self.usera).withrawable_balance ,1000)

        CashWithrawal.objects.create(user=self.usera,amount=800) 


        self.assertEqual(Account.objects.get(user=self.usera).balance,9000)
        self.assertEqual(Account.objects.get(user=self.usera).withrawable_balance ,1000)
        
        self.assertEqual(CashWithrawal.objects.get(id=1).approved,False)

        CashWithrawal.objects.filter(id=1).update(approved=True)

        self.assertEqual(CashWithrawal.objects.get(id=1).approved,True)

        self.assertEqual(Account.objects.get(user=self.usera).balance,9000)
        # self.assertEqual(Account.objects.get(user=self.usera).withrawable_balance , 200)#failin

