from django.test import TestCase
from users.models import User
from .models import Istake, CashStore, IoutCome
from account.models import Account, CashDeposit


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

    def test_store_bank_mat(self):
        # CashStore.objects.create(id=1)
        Istake.objects.create(user=self.user, amount=1000)
        # give_away = IoutCome.objects.get(stake=stak).cashstore.give_away
        cas = CashStore.objects.get(id=1)
        
        self.assertEqual(cas.give_away, 1000)

        Istake.objects.create(user=self.user, amount=1000)
        cas = CashStore.objects.get(id=1)

        self.assertEqual(cas.give_away, 2000)

        Istake.objects.create(user=self.user, amount=1000)
        cas = CashStore.objects.get(id=1)

        self.assertEqual(cas.give_away, 3000)

        Istake.objects.create(user=self.user, amount=1000)
        cas = CashStore.objects.get(id=1)

        self.assertEqual(cas.give_away, 2000)        

        Istake.objects.create(user=self.user, amount=100)
        cas = CashStore.objects.get(id=1)

        self.assertEqual(cas.give_away, 1900)

        Istake.objects.create(user=self.user, amount=500)
        cas = CashStore.objects.get(id=1)

        self.assertEqual(cas.give_away, 1400)

        Istake.objects.create(user=self.user, amount=1100)
        cas = CashStore.objects.get(id=1)

        self.assertEqual(cas.give_away, 2500)        