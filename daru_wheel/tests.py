from django.test import TestCase
from users.models import User
import random
from django.utils import timezone
from time import sleep
from daru_wheel.models import (
    Stake, CashStore, OutCome, Market, WheelSpin, Selection,
    current_account_trialbal_of,)

from account.models import Account, CashDeposit ,current_account_bal_of
# MODEL TESTS

def create_user():
    return User.objects.create(username="0725100876",email='user12@mail.com',daru_code="ADMIN")


def create_test_user(username):
    '''simplify create_test_user'''  
    ran_value = random.randint(1, 99)
    email = f'user{ran_value}@darucasino.com' 

    return User.objects.create(
        username=str(username),
        email=email,
        daru_code="ADMIN") 


def deposit_to_test_user(user_id, amount=10000):
    CashDeposit.objects.create(
        user_id=user_id,
        amount=amount) 

class MarketTestCase(TestCase):
    def test_create_rit_market(self):

        WheelSpin.objects.create()
        WheelSpin.objects.create()


        self.assertEqual(Market.objects.count(), 1)
        

class StakeTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        CashDeposit.objects.create(user=self.user, amount=10000)  
        self.spin = WheelSpin.objects.create()        
        self.market = Market.objects.get(id=1)

        market = WheelSpin.objects.create()

        self.marketselection1, _ = Selection.objects.get_or_create(
            id=1,
            mrtype=self.market,
            name='RED',
            odds=2)

        self.marketselection2, _ = Selection.objects.get_or_create(
            id=2,
            mrtype=self.market,
            name='YELLOW',
            odds=2)

    
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

        stake1=Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection1,
            bet_on_real_account=True, amount=1000) #REAL
        OutCome.objects.create(stake_id=stake1.id)
        stake2 = Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection2,
            amount=1000) #TRIAL
        OutCome.objects.create(stake_id=stake2.id)

        self.assertEqual(OutCome.objects.count(), 2)
        self.assertEqual(current_account_bal_of(self.user), 9000)
        self.assertEqual(current_account_trialbal_of(self.user), 49000)       
        self.assertEqual(CashStore.objects.get(id=1).give_away, 1000)

    #     #______________________________________________

        stake=Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection2,
            bet_on_real_account=True, amount=1000)  #REAL
        OutCome.objects.create(stake_id=stake.id)
        stake =Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection1,
            bet_on_real_account=False, amount=2000) # TRIAL
        OutCome.objects.create(stake_id=stake.id)

        self.assertEqual(OutCome.objects.count(), 4) 
        self.assertEqual(current_account_bal_of(self.user), 8000)
        self.assertEqual(current_account_trialbal_of(self.user), 47000)
        self.assertEqual(CashStore.objects.get(id=1).give_away, 2000)

    #     #_____________________________________________________

        stake =Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection1,
            bet_on_real_account=True, amount=1000)

        OutCome.objects.create(stake_id=stake.id)
        stake=Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection2,
            bet_on_real_account=False, amount=5000)
        OutCome.objects.create(stake_id=stake.id)
        
        self.assertEqual(OutCome.objects.count(), 6)
        self.assertEqual(current_account_bal_of(self.user), 7000)
        self.assertEqual(current_account_trialbal_of(self.user), 42000)
        self.assertEqual(CashStore.objects.get(id=1).give_away, 3000)

    #     #_____________________________________________

        stake =Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection2,
            bet_on_real_account=True, amount=1000)
        OutCome.objects.create(stake_id=stake.id)

        stake =Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection1, amount=1000)
        OutCome.objects.create(stake_id=stake.id)    
   
        # self.assertEqual(OutCome.objects.count(), 7)
        self.assertEqual(current_account_bal_of(self.user), 8000)
        self.assertEqual(current_account_trialbal_of(self.user), 41000)
        self.assertEqual(CashStore.objects.get(id=1).give_away, 2000)   
    #     #_______________________________________________________________  

        stake =Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection1,
            bet_on_real_account=True, amount=100)
        OutCome.objects.create(stake_id=stake.id)

        self.assertEqual(CashStore.objects.get(id=1).give_away, 1900)

        stake =Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection1,
            bet_on_real_account=True, amount=500)
        OutCome.objects.create(stake_id=stake.id)

        self.assertEqual(CashStore.objects.get(id=1).give_away, 1400)

    #     #________________________________________________

        stake =Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection1,
            bet_on_real_account=True, amount=1100)
        OutCome.objects.create(stake_id=stake.id)

        self.assertEqual(current_account_bal_of(self.user), 7500)
        self.assertEqual(current_account_trialbal_of(self.user), 41000)

        self.assertEqual(CashStore.objects.get(id=1).give_away, 2500)  

    def test_create_stake_for_rit_market(self):
        self.spin = WheelSpin.objects.create()        
        self.market = Market.objects.get(id=1)

        market = WheelSpin.objects.create()

        self.marketselection1, _ = Selection.objects.get_or_create(
            id=1,
            mrtype=self.market,
            name='RED',
            odds=2)

        self.marketselection2, _ = Selection.objects.get_or_create(
            id=2,
            mrtype=self.market,
            name='YELLOW',
            odds=2)



        Stake.objects.create(
            user=self.user,
            market=self.spin,
            bet_on_real_account=False,
            amount=100)

        self.assertEqual(OutCome.objects.count(), 0)


        stake=Stake.objects.create(
            user=self.user,
            marketselection=self.marketselection1,
            bet_on_real_account=False,
            amount=100)

        OutCome.objects.create(stake_id=stake.id)    
            
        self.assertEqual(OutCome.objects.count(), 1)




# class LoginPageTest(TestCase):

#     TEST_USERNAME = '0721399876'
#     TEST_EMAIL = 'john@casino.test'
#     TEST_PASSWORD = 'Tw0jaStaraZ4pierdala'

#     def test_user_can_login_with_valid_data(self):
#         User.objects.create_user(username=self.TEST_USERNAME,
#                                  email=self.TEST_EMAIL,
#                                  password=self.TEST_PASSWORD)
#         response = self.client.post('/user/login', {
#             'username': self.TEST_USERNAME,
#             'password': self.TEST_PASSWORD
#         })
#         self.assertRedirects(response, '/')

# # class SpinPageTest(TestCase):
# #     def test_spin_home_template(self):
# #         response = self.client.get('/daru_wheel/spin')
# #         self.assertRedirects(response, '/user/login?next=/daru_wheel/spin')
        
# #         # self.assertTemplateUsed(response, 'home.html')


class BetLogicTest(TestCase):

    def setUp(self):
        self.spin = WheelSpin.objects.create()        
        self.market = Market.objects.get(id=1)
        

        self.marketselection1, _ = Selection.objects.get_or_create(
            id=1,
            mrtype=self.market,
            name='RED',
            odds=2)

        self.marketselection2, _ = Selection.objects.get_or_create(
            id=2,
            mrtype=self.market,
            name='YELLOW',
            odds=2)

        self.user1 = create_test_user('07000000001')
        self.user2 = create_test_user('07000000002')
        self.user3 = create_test_user('07000000003')

        deposit_to_test_user(self.user1.id, 5000)
        deposit_to_test_user(self.user2.id, 6000)
        deposit_to_test_user(self.user3.id, 1000)
  

    def test_setup(self):        
        self.assertEqual(
            current_account_bal_of(self.user1.id),
            5000)

        self.assertEqual(
            current_account_bal_of(self.user2.id),
            6000)

        self.assertEqual(
            current_account_bal_of(self.user3.id),
            1000)

        self.assertEqual(Market.objects.count(),1)    
  
        # BET
    def test_test_deduct_bet_amount(self):  
        #BEFORE  
        self.assertEqual(
            current_account_bal_of(self.user1.id),
            5000)

        self.assertEqual(
            current_account_bal_of(self.user2.id),
            6000)
            
        self.assertEqual(
            current_account_bal_of(self.user3.id),
            1000)        
        #BET
        Stake.objects.create(
            user=self.user1,
            market=self.spin,
            marketselection=self.marketselection1,
            bet_on_real_account=True,
            amount=100)

        Stake.objects.create(
            user=self.user2,
            market=self.spin,
            marketselection=self.marketselection2,
            bet_on_real_account=True,
            amount=200)

        Stake.objects.create(
            user=self.user3,
            market=self.spin,
            marketselection=self.marketselection1,
            bet_on_real_account=True,
            amount=300)

        #AFTER
        self.assertEqual(
            current_account_bal_of(self.user1.id),
            4900)

        self.assertEqual(
            current_account_bal_of(self.user2.id),
            5800)

    def test_test_add_winner_account_amount(self):  #1
        '''#1 test/let it not failed: It determine precise stake culculations'''
        #BEFORE  
        self.assertEqual(
            current_account_bal_of(self.user1.id),
            5000)

        self.assertEqual(
            current_account_bal_of(self.user2.id),
            6000)
            
        self.assertEqual(
            current_account_bal_of(self.user3.id),
            1000)        
        #BET
        Stake.objects.create(
            user=self.user1,
            market=self.spin,
            marketselection=self.marketselection1,
            bet_on_real_account=True,
            amount=1000)

        Stake.objects.create(
            user=self.user2,
            market=self.spin,
            marketselection=self.marketselection2,
            bet_on_real_account=True,
            amount=200)

        Stake.objects.create(
            user=self.user3,
            market=self.spin,
            marketselection=self.marketselection2,
            bet_on_real_account=False,
            amount=300)

        #AFTER
        self.assertEqual(
            current_account_bal_of(self.user1.id),
            4000)

        self.assertEqual(
            current_account_bal_of(self.user2.id),
            5800)
        self.assertEqual(
            current_account_bal_of(self.user3.id),
            1000)
        self.assertEqual(
            current_account_trialbal_of(self.user3.id),
            49700)       
  
        #OUTCOME

        outcome = OutCome.objects.create(market=self.spin)

        self.assertEqual(OutCome.objects.count(),1 )
        self.assertEqual(outcome.result,2 )



        #AFTER OUTCOME
        self.assertEqual(
            current_account_bal_of(self.user1.id),
            4000)

        self.assertEqual(
            current_account_bal_of(self.user2.id),
            6200)

        self.assertEqual(
            current_account_bal_of(self.user3.id),
            1000)

        self.assertEqual(
            current_account_trialbal_of(self.user3.id),
            50300)

    def test_total_bet_amount_per_market(self):
             #BET
        Stake.objects.create(
            user=self.user1,
            market=self.spin,
            marketselection=self.marketselection1,
            bet_on_real_account=False,
            amount=100)

        Stake.objects.create(
            user=self.user2,
            market=self.spin,
            marketselection=self.marketselection2,
            bet_on_real_account=True,
            amount=200)

        Stake.objects.create(
            user=self.user3,
            market=self.spin,
            marketselection=self.marketselection1,
            bet_on_real_account=True,
            amount=300)

        Stake.objects.create(
            user=self.user1,
            market=self.spin,
            marketselection=self.marketselection1,
            bet_on_real_account=True,
            amount=150)

        Stake.objects.create(
            user=self.user2,
            market=self.spin,
            marketselection=self.marketselection2,
            bet_on_real_account=False,
            amount=600)
        #MARKET STATE
        self.assertEqual(self.spin.selection_bet_amount,[450,200]) 


# # TEST VIEWS





# # class DaruWeelTest(TestCase):

# #     def test_uses_seed_template(self):
# #         response = self.client.get('/daru_wheel/spin')
# #         print('RESSS',response)
# #         self.assertTemplateUsed(response, 'daru_wheel/ispin.html')