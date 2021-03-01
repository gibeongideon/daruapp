from django.test import TestCase  #,Client
from django.urls import reverse
from account.models import CashDeposit, CashWithrawal, Account
from users.models import User
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