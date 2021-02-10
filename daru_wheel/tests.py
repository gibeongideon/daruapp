from django.test import TestCase
from users.models import User
from .models import Istake
from account.models import  Account,CashDeposit

# Create your tests here.

def create_user():
    return User.objects.create(username="testuser1",phone_number="0710010000")

class IstakeTestCase(TestCase):
    def setUp(self):
        self.user = create_user()

    
    def test_no_balance_bet(self):        
        Istake.objects.create(user=self.user, amount=100)
        Istake.objects.create(user=self.user, amount=100, bet_on_real_account=True )
        stakecount = Istake.objects.count()

        self.assertEqual(stakecount, 1)

    def test_neative_bet(self):
        Istake.objects.create(user=self.user, amount=-100)
        Istake.objects.create(user=self.user, amount=-100, bet_on_real_account=True )
        stakecount = Istake.objects.count()
        self.assertEqual(stakecount, 0)

        Istake.objects.create(user=self.user, amount=100)
        Istake.objects.create(user=self.user, amount=100, bet_on_real_account=True )
        stakecount = Istake.objects.count()
        self.assertEqual(stakecount, 1)
    
    def test_cannot_bet_more_tan_balance(self):
        CashDeposit.objects.create(user=self.user, amount=1000)
        Istake.objects.create(user=self.user, amount=1000)
        Istake.objects.create(user=self.user, amount=100000)
        stakecount = Istake.objects.count()
        self.assertEqual(stakecount, 1)
        Istake.objects.create(user=self.user, amount=9000)
        stakecount = Istake.objects.count()
        self.assertEqual(stakecount, 2)

