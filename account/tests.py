from django.test import TestCase  #,Client
from django.urls import reverse
from .models import CashDeposit, CashWithrawal, Account
from users.models import User

class CashDepositWithrawalTestCase(TestCase):
    def setUp(self):
       self.usera=User.objects.create(username="test_usera", email="testa@gmail.com", phone_number="1111111111")
       self.userb=User.objects.create(username="test_userb", email="testb@gmail.com", phone_number="2222222222")
      
    def test_user_deposit(self):
        CashDeposit.objects.create(amount=1000,user=self.usera)
        bal1a = Account.objects.get(user=self.usera).balance
        bal1b = Account.objects.get(user=self.userb).balance
        

        self.assertEqual(1000, bal1a)
        self.assertEqual(0, bal1b)

        CashDeposit.objects.create(amount=100000,user=self.usera)
        CashDeposit.objects.create(amount=1000,user=self.userb)
        bal2a = Account.objects.get(user=self.usera).balance
        bal2b = Account.objects.get(user=self.userb).balance

        self.assertEqual(101000, bal2a)
        self.assertEqual(1000, bal2b)

        



