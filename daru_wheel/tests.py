from django.test import TestCase
from users.models import User
from .models import Istake, CashStore, IoutCome ,current_account_trialbal_of
from account.models import Account, CashDeposit ,current_account_bal_of


# Create your tests here.

def create_user():
    return User.objects.create(username="testuser1",phone_number="0710010000")


class IstakeTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        CashDeposit.objects.create(user=self.user,amount=10000) 
        
    
    def test_no_balance_bet(self):
        
        bal= current_account_bal_of(self.user.id)
        tbal=current_account_trialbal_of(self.user.id)

        self.assertEqual(bal,10000)    
        self.assertEqual(tbal,50000) 

        Istake.objects.create(user=self.user, amount=1000)
        Istake.objects.create(user=self.user, amount=60000)
        self.assertEqual(bal, 10000 )
        Istake.objects.create(user=self.user, bet_on_real_account=True, amount=1000)
        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=20000)
        stakecount = Istake.objects.count()

        self.assertEqual(stakecount, 2)

    def test_neative_bet(self):
        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=-100)
        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=-100)
        stakecount = Istake.objects.count()
        self.assertEqual(stakecount, 0)

        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=100)
        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=100)
        stakecount = Istake.objects.count()
        self.assertEqual(stakecount, 2)
    
    def test_cannot_bet_more_tan_balance(self):
        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=1000)
        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=100000)
        stakecount = Istake.objects.count()
        self.assertEqual(stakecount, 1)
        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=9000)
        Istake.objects.create(user=self.user, amount=90000)
        stakecount = Istake.objects.count()
        self.assertEqual(stakecount, 2)

    def test_store_bank_mat(self):
        # CashStore.objects.create(id=1)

        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=1000) #REAL
        Istake.objects.create(user=self.user, amount=1000) #TRIAL

        cas = CashStore.objects.get(id=1)
        user_bal= current_account_bal_of(self.user)
        user_trialbal= current_account_trialbal_of(self.user)

        self.assertEqual(user_bal, 9000)
        self.assertEqual(user_trialbal, 49000)
        
        self.assertEqual(cas.give_away, 1000)

        #______________________________________________

        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=1000)  #REAL
        Istake.objects.create(user=self.user,bet_on_real_account=False, amount=2000) # TRIAL

        cas = CashStore.objects.get(id=1)
        user_bal= current_account_bal_of(self.user)
        user_trialbal= current_account_trialbal_of(self.user)

        self.assertEqual(user_bal, 8000)
        self.assertEqual(user_trialbal, 47000)

        self.assertEqual(cas.give_away, 2000)

        #_____________________________________________________

        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=1000)
        Istake.objects.create(user=self.user,bet_on_real_account=False, amount=5000)

        cas = CashStore.objects.get(id=1)


        user_bal= current_account_bal_of(self.user)
        user_trialbal= current_account_trialbal_of(self.user)

        self.assertEqual(user_bal, 7000)
        self.assertEqual(user_trialbal, 42000)

        self.assertEqual(cas.give_away, 3000)


        #_____________________________________________

        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=1000)
        Istake.objects.create(user=self.user, amount=1000)
        cas = CashStore.objects.get(id=1)

        user_bal= current_account_bal_of(self.user)
        user_trialbal= current_account_trialbal_of(self.user)

        self.assertEqual(user_bal, 8000)
        self.assertEqual(user_trialbal, 41000)

        self.assertEqual(cas.give_away, 2000)   
        #_______________________________________________________________  

        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=100)
        cas = CashStore.objects.get(id=1)

        self.assertEqual(cas.give_away, 1900)

        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=500)
        cas = CashStore.objects.get(id=1)

        self.assertEqual(cas.give_away, 1400)

        #________________________________________________

        Istake.objects.create(user=self.user,bet_on_real_account=True, amount=1100)
        cas = CashStore.objects.get(id=1)

        user_bal= current_account_bal_of(self.user)
        user_trialbal= current_account_trialbal_of(self.user)

        self.assertEqual(user_bal, 7500)
        self.assertEqual(user_trialbal, 41000)

        self.assertEqual(cas.give_away, 2500)  

