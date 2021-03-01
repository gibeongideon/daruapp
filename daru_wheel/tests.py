from django.test import TestCase
from users.models import User
from daru_wheel.models import Stake, CashStore, OutCome ,current_account_trialbal_of,Market ,WheelSpin,DaruPoker,MarketType
from account.models import Account, CashDeposit ,current_account_bal_of
# MODEL TESTS

def create_user():
    return User.objects.create(username="0725100876",email='user12@mail.com',daru_code="ADMIN")

class MarketTestCase(TestCase):
    def test_create_rit_market(self):

        WheelSpin.objects.create()
        WheelSpin.objects.create()
        DaruPoker.objects.create()

        self.assertEqual(Market.objects.count(), 3)
        

class StakeTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        CashDeposit.objects.create(user=self.user, amount=10000)        
    
    def test_no_balance_bet(self):

        self.assertEqual(current_account_bal_of(self.user.id),10000)    
        self.assertEqual(current_account_trialbal_of(self.user.id),50000) 

        Stake.objects.create(user=self.user, amount=1000)
        Stake.objects.create(user=self.user, amount=60000)

        self.assertEqual(current_account_bal_of(self.user.id), 10000 )

        Stake.objects.create(user=self.user, bet_on_real_account=True, amount=1000)
        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=20000)
  
        self.assertEqual(Stake.objects.count(), 2)

    def test_neative_bet(self):
        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=-100)
        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=-100)
     
        self.assertEqual(Stake.objects.count(), 0)

        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=100)
        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=100)

        self.assertEqual(Stake.objects.count(), 2)
    
    def test_cannot_bet_more_tan_balance(self):
        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=1000)
        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=100000)

        self.assertEqual(Stake.objects.count(), 1)
        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=9000)
        Stake.objects.create(user=self.user, amount=90000)

        self.assertEqual(Stake.objects.count(), 2)

    def test_store_bank_mat(self):

        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=1000) #REAL
        Stake.objects.create(user=self.user, amount=1000) #TRIAL
     
        self.assertEqual(current_account_bal_of(self.user), 9000)
        self.assertEqual(current_account_trialbal_of(self.user), 49000)
        
        self.assertEqual(CashStore.objects.get(id=1).give_away, 1000)

        #______________________________________________

        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=1000)  #REAL
        Stake.objects.create(user=self.user,bet_on_real_account=False, amount=2000) # TRIAL

        self.assertEqual(current_account_bal_of(self.user), 8000)
        self.assertEqual(current_account_trialbal_of(self.user), 47000)

        self.assertEqual(CashStore.objects.get(id=1).give_away, 2000)

        #_____________________________________________________

        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=1000)
        Stake.objects.create(user=self.user,bet_on_real_account=False, amount=5000)

        self.assertEqual(current_account_bal_of(self.user), 7000)
        self.assertEqual(current_account_trialbal_of(self.user), 42000)

        self.assertEqual(CashStore.objects.get(id=1).give_away, 3000)

        #_____________________________________________

        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=1000)
        Stake.objects.create(user=self.user, amount=1000)
   

        self.assertEqual(current_account_bal_of(self.user), 8000)
        self.assertEqual(current_account_trialbal_of(self.user), 41000)

        self.assertEqual(CashStore.objects.get(id=1).give_away, 2000)   
        #_______________________________________________________________  

        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=100)

        self.assertEqual(CashStore.objects.get(id=1).give_away, 1900)

        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=500)

        self.assertEqual(CashStore.objects.get(id=1).give_away, 1400)

        #________________________________________________

        Stake.objects.create(user=self.user,bet_on_real_account=True, amount=1100)

        self.assertEqual(current_account_bal_of(self.user), 7500)
        self.assertEqual(current_account_trialbal_of(self.user), 41000)

        self.assertEqual(CashStore.objects.get(id=1).give_away, 2500)  

    def test_create_stake_for_rit_market(self):
        market_type = MarketType.objects.create(name='SPIN')
        market = Market.objects.create(market_type=market_type)

        Stake.objects.create(
            user=self.user,
            market=market,
            bet_on_real_account=False,
            amount=100)

        self.assertEqual(OutCome.objects.count(), 0)

        Stake.objects.create(
            user=self.user,
            bet_on_real_account=False,
            amount=100)
            
        self.assertEqual(OutCome.objects.count(), 1)




# TEST VIEW


# class BetViewTest(TestCase):
#     def test_can_bet_istake_request(self):
#         self.user = create_user()
#         self.client.post(
#             "spin",
#             data={'user': self.user,'marketselection':1,'amount':333}
#             )
#         self.assertEqual(Stake.objects.count(), 1)

class LoginPageTest(TestCase):

    TEST_USERNAME = '0721399876'
    TEST_EMAIL = 'john@casino.test'
    TEST_PASSWORD = 'Tw0jaStaraZ4pierdala'

    def test_user_can_login_with_valid_data(self):
        User.objects.create_user(username=self.TEST_USERNAME,
                                 email=self.TEST_EMAIL,
                                 password=self.TEST_PASSWORD)
        response = self.client.post('/user/login', {
            'username': self.TEST_USERNAME,
            'password': self.TEST_PASSWORD
        })
        self.assertRedirects(response, '/')

class SpinPageTest(TestCase):
    def test_spin_home_template(self):
        response = self.client.get('/daru_wheel/spin')
        self.assertRedirects(response, '/user/login?next=/daru_wheel/spin')
        
        # self.assertTemplateUsed(response, 'home.html')


