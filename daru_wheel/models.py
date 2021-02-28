from django.db import models
from django.conf import settings
from django.db.models import Sum
from datetime import timedelta, datetime
from random import randint
from django.utils import timezone
try:
    from account.models import RefCredit
    from account.models import (
        update_account_bal_of,
        log_record, refer_credit_create)
except ImportError as e:
    pass

from django.contrib.auth import get_user_model
User = get_user_model() # make apps independent
# from .tasks import create_market


def current_account_bal_of(user_id): #F2
    from account.models import Account
    try:
        return float(Account.objects.get(user_id =user_id).balance)
    except Exception as e:
        return e

def current_account_trialbal_of(user_id): #F2
    from account.models import Account
    try:
        return float(Account.objects.get(user_id =user_id).trial_balance)
    except Exception as e:
        return e

def update_account_trialbal_of(user_id,new_bal): #F3
    from account.models import Account
    try:
        if new_bal >= 0:
            Account.objects.filter(user_id =user_id).update(trial_balance= new_bal)
        else:
            log_record(user_id,0,'Account Error') # REMOVE
    except Exception as e:
        return e


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    # is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class DaruWheelSetting(TimeStamp):
    return_val = models.FloatField(default=0, blank=True, null=True)
    min_redeem_refer_credit = models.FloatField(default=1000, blank=True, null=True)
    refer_per = models.FloatField(default=0, blank=True, null=True)
    closed_at = models.FloatField(
        help_text='sensitive settings value.Dont edit',
        default=4.7, blank=True, null=True)
    results_at = models.FloatField(
        help_text='sensitive settings value.Dont edit',
        default=4.8, blank=True, null=True)
    wheelspin_id = models.IntegerField(
        help_text='super critical setting value.DONT EDIT!',
        default=1, blank=True, null=True)
    curr_unit = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    min_bet = models.DecimalField(max_digits=5,default=45.9, decimal_places=2, blank=True, null=True)
    
    class Meta:
        db_table = "d_daruwheel_setup"


try:
    ''' remove no such table on make migrations'''
    set_up, created = DaruWheelSetting.objects.get_or_create(id=1)  # fail save
except Exception as me:
    print("MEE", me)
    pass


class MarketType(TimeStamp):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return '{0}:{1}'.format(self.id, self.name)

    def all_selection(self):
        return Selection.objects.filter(mrtype_id=self.id).all()

    def this_market_selection_id_list(self):
        return [_mselect.id for _mselect in self.all_selection() ]

    def this_market_selection_verbose_list(self):
        return [(_mselect.id, _mselect.name, _mselect.odds) for _mselect in self.all_selection()]


class Market(models.Model):
    '''Market place wit different market types  '''
    market_type = models.ForeignKey(
        MarketType,
        on_delete=models.CASCADE,
        related_name='market_types', blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)
    receive_results = models.BooleanField(default=False, blank=True, null=True)

    # class Meta:
    #     abstract = True

    def __str__(self):
        return f'{self.market_type.name}:{self.id} '



class Selection(TimeStamp):
    mrtype = models.ForeignKey(
        MarketType, on_delete=models.CASCADE,
        related_name='mrtypes', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    odds = models.FloatField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def market_id(self):
        return self.mrtype
     

class DaruPoker(TimeStamp):
    ''' Create DaruPoker market Instance '''
    market = models.OneToOneField(
        Market, on_delete=models.CASCADE,
        related_name='poker_markets', blank=True, null=True)
        
    class Meta:
        db_table = "d_poker_markets"


class WheelSpin(TimeStamp):
    '''Create WheelSpin market instance'''
    market = models.OneToOneField(
        Market,
        on_delete=models.CASCADE,
        related_name='markets', blank=True, null=True)

    open_at = models.DateTimeField(default=timezone.now, blank=True, null=True) 
    closed_at = models.DateTimeField(blank=True, null=True)
    results_at = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)
    per_retun = models.FloatField(default=0, blank=True, null=True)

    class Meta:
        db_table = "d_wheel_markets"

    def __str__(self):
        return f'WheelSpin No:{self.id}'

    @property
    def place_stake_is_active(self):
        try:
            if timezone.now() > self.open_at and timezone.now() < self.closed_at:
                return True
            return False
        except Exception as e:
            return e

    @property
    def get_result_active(self):
        try:
            if timezone.now() > self.results_at:
                return True
            return False
        except Exception as e:
            return e


    def market_selection_id_list(self):
        try:
            return self.market.market_type.this_market_selection_id_list()
        except Exception as e:
            return e    

    def total_bet_amount_per_marktinstance(self):
        try:
            total_amount = Stake.objects.filter(market_id =self.id ).aggregate(bet_amount=Sum('amount'))
            return total_amount.get('bet_amount')

        except Exception as e:
            return e

    @property
    def black_bet_amount(self):
        try:
            total_amount = Stake.objects.filter(market_id = self.id ).filter(marketselection_id = 1).aggregate(bet_amount =Sum('amount'))
            if total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
            return 0
            
        except Exception as e:
            return e

    @property
    def white_bet_amount(self):

        try:
            total_amount = Stake.objects.filter(market_id =self.id ).filter(marketselection_id =2).aggregate(bet_amount =Sum('amount'))
            if  total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
            return 0
            
        except Exception as e:
            return e

    def market_stake_amount(self, select_id):

        try:
            total_amount = Stake.objects.filter(market_id =self.id ).filter(marketselection_id =select_id).aggregate(bet_amount =Sum('amount'))
            if  total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
            return 0
        
        except Exception as e:
            return e

    @property
    def selection_bet_amount(self):
        try:
            mrkt_bet_amount = []
            for selecn in self.market.market_type.this_market_selection_id_list():
                mrkt_bet_amount.append(self.market_stake_amount(selecn))
            return mrkt_bet_amount
        except Exception as e:
            return e


    @property
    def offset(self):
        try:
            return abs(self.white_bet_amount - self.black_bet_amount)

        except Exception as e:
            return e

    @property
    def gain_after_relief(self):
        per_to_return = self.per_retun
        return ((100 - per_to_return)/100)*float(self.offset)

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on staking  '''
        
        self.closed_at = self.open_at + timedelta(minutes=set_up.closed_at)
        self.results_at = self.open_at + timedelta(minutes=set_up.results_at)

        if self.active and not self.place_stake_is_active:
            self.active = False
        # try:
        #     self.market,_ = MarketType.objects.get_or_create( id= int(set_up.wheelspin_id ) )#get_or_create return a tuple/
        # except:
        #     self.market,_ = MarketType.objects.get_or_create( id= 1)
            
        super().save(*args, **kwargs)

  
class Stake (TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_wp_stakes',blank =True,null=True)
    market = models.ForeignKey(WheelSpin, on_delete=models.CASCADE,related_name='wheelspins',blank =True,null=True)
    marketselection = models.ForeignKey(Selection, on_delete=models.CASCADE,related_name='marketselections',blank =True,null=True)
    current_bal = models.FloatField(max_length=10,default=0 )#R
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    stake_placed = models.BooleanField(blank =True,null=True)
    has_record = models.BooleanField(blank =True,null=True)

    def __str__(self):
        return 'Stake:{0} for:{1}'.format(self.amount,self.user)  


    @classmethod
    def per_market_bets(cls,market_id):
        return cls.objects.filter(market_id = market_id)

    @property
    def place_bet_is_active(self):
        return self.market.place_stake_is_active
        
    @property
    def status(self):
        return self.update_account_on_win_lose()

    def update_account_on_win_lose(self):
        selection = self.marketselection_id
        try:
            results = Result.objects.get(market_id = self.market_id).resu  #self.marketinstant.determine_result_algo
        except:
            results = ''
        resu = ''
        try:
            if not results:
                resu = 'PENDING'               
            elif selection == results:
                resu= 'YOU WIN'
            else:
                resu = 'YOU LOSE'
            return resu
            
        except Exception as e:
            print('GERR',e)


    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on staking  '''
        if not self.stake_placed:
            try:
                market_id = max((obj.id for obj in WheelSpin.objects.all()))
                this_wheelspin = WheelSpin.objects.get(id =market_id )
            except Exception as mae:
                this_wheelspin,_ = WheelSpin.objects.get_or_create(id =1)
                pass
                  

            if this_wheelspin.place_stake_is_active:# 

                self.market = this_wheelspin
                try:
                    current_user_account_bal = current_account_bal_of(self.user.id) # F2
                    if self.amount <= current_user_account_bal: # no staking more than account balance
                        if not self.stake_placed:
                            new_bal = current_user_account_bal - float(self.amount)
                            self.current_bal = new_bal
                            update_account_bal_of(self.user_id,new_bal)# F3
                            self.stake_placed = True
                    
                    else: 
                        raise Exception ('insufficient funds')
                        # return 'Not enough balance to stake'

                except Exception as e:
                    print('STAKE:',e)
                    return e
            else:
                print('INACTIVE MARKET!')
                return # no saving record if market is inactive

            try:
                if not self.has_record:
                    log_record(self.user_id,self.amount,'Stake')
                    
                    self.has_record = True
            except:
                pass

            super().save(*args, **kwargs)

class CumulativeGain(TimeStamp):

    gain = models.FloatField(default=0, blank =True,null= True)

    @property
    def gainovertime(self): 

        try:
            total_amount = Result.objects.filter(cumgain_id = self.id ).aggregate(cum_amount =Sum('gain'))
            if  total_amount.get('cum_amount'):
                return total_amount.get('cum_amount')
            return total_amount
            
        except Exception as e:
            return e

class OutCome(TimeStamp):
    market  = models.OneToOneField(WheelSpin,on_delete=models.CASCADE,related_name='marketoutcomes',blank =True,null= True)
    result = models.IntegerField(blank =True,null= True)
    pointer = models.IntegerField(blank =True,null= True)
    closed = models.BooleanField(default = False,blank =True,null= True)

    @property
    def determine_result_algo(self):  # fix this
        try:
            B = self.market.black_bet_amount
            W = self.market.white_bet_amount
            
            if self.market.place_stake_is_active == False:
                if B == W:
                    return randint(1,2) # fix me to get random 1 or 2
                if B > W :
                    return 2
                return 1

        except Exception as e:
            return  e

    @staticmethod
    def result_to_segment(results = None, segment=29):
        from random import randint, randrange
        if results is None:
            results = randint(1,2)
        if results ==1:
            return randrange(1,segment,2) # odd no b/w 1 to segment(29)
        else:
            return randrange(2,segment,2) # even no b/w 2 to segment(29)
            
    @property
    def segment(self):
        return self.result_to_segment(results = self.result)# ,segment = 29) from settings

    def save(self, *args, **kwargs):
        if not self.closed:
            if self.market.place_stake_is_active == False:
                self.result = self.determine_result_algo
                self.pointer = self.segment
                self.closed =True

                super().save(*args, **kwargs)
        else:
            return

class Result(TimeStamp):
    market = models.OneToOneField(WheelSpin,on_delete=models.CASCADE,related_name='rmarkets',blank =True,null= True)
    cumgain = models.ForeignKey(CumulativeGain,on_delete=models.CASCADE,related_name='gains',blank =True,null= True)

    resu = models.IntegerField(blank =True,null= True)

    return_per =models.FloatField(blank =True,null= True)
    gain = models.DecimalField(('gain'), max_digits=100, decimal_places=5,blank =True,null= True)

    closed = models.BooleanField(blank =True,null= True)
    active = models.BooleanField(blank =True,null= True)

    @property
    def determine_result_algo(self):  # fix this
        try:
            B = self.market.black_bet_amount
            W = self.market.white_bet_amount
            
            if self.market.place_stake_is_active == False:
                if B == W:
                    return randint(1,2) # fix me to get random 1 or 2
                if B > W :
                    return 2
                return 1

        except Exception as e:
            return  e

    @staticmethod
    def per_return_relief(all_gain,userstake,all_lose_stake,per_to_return):  ##CRITICAL FUCTION/MUST WORK PROPERLY
        try:
            return_amount = (per_to_return/100)*all_gain
            per_user_return = (userstake/all_lose_stake)*return_amount
            return per_user_return

        except Exception as e:
            return 0

    @staticmethod
    def update_reference_account(user_id,ref_credit,trans_type):
        print(user_id,ref_credit,trans_type)

        try:
            this_user = User.objects.get(id = user_id)
         
            this_user_ReferCode = this_user.daru_code # first name is used as referer code
            if not this_user_ReferCode:
                this_user_ReferCode = 'ADMIN'  # settings
            
            referer_users = User.objects.filter(my_code = this_user_ReferCode)
            for referer in referer_users:
                print(referer,'RefererUser')

                refer_credit_create(referer,this_user.username,ref_credit) #F4
                # log_record(referer.id,ref_credit,'ref_credit') # F1 Redundant

        except Exception as e:
            print('update_reference_account ERROR',e)

    @staticmethod
    def update_acc_n_bal_record(user_id,new_bal,rem_credit,trans_type):
        try: 
            update_account_bal_of(user_id,new_bal) #F3       
            log_record(user_id,rem_credit,trans_type) #F1
        except Exception as e:

            print('update_acc_n_bal_record ERROR',e)

    def update_winner_losser(self,this_user_stak_obj):
        user_id = this_user_stak_obj.user_id
        user_current_account_bal =current_account_bal_of(user_id)

        #WINNER 
        if this_user_stak_obj.marketselection_id == self.resu:
            amount = float(this_user_stak_obj.amount)
            odds = float(this_user_stak_obj.marketselection.odds)
            per_for_referer = set_up.refer_per  # Settings
            print(f'REFFC:{per_for_referer}')
            win_amount = amount *odds

            if per_for_referer > 100: # Enforce 0<=p<=100 TODO
                per_for_referer = 0

            ref_credit = (per_for_referer/100)*win_amount
            rem_credit = win_amount -ref_credit

            new_bal = user_current_account_bal + rem_credit

            trans_type = 'WIN' 
            self.update_acc_n_bal_record(user_id,new_bal,rem_credit,trans_type)

            if ref_credit > 0:
                trans_type = 'R-WIN'
                self.update_reference_account(user_id,ref_credit,trans_type)

        #LOSER
        elif this_user_stak_obj.marketselection_id != self.resu:
            all_gain = float(self.market.offset) # FIX
            userstake =  float(this_user_stak_obj.amount)
 
            if self.resu == 2:
                all_lose_stake = float(self.market.black_bet_amount)
            elif self.resu ==1:
                all_lose_stake = float(self.market.white_bet_amount)

            per_to_return = float(self.market.per_retun) # 
            relief_amount = self.per_return_relief(all_gain,userstake,all_lose_stake,per_to_return)

            new_bal = user_current_account_bal + relief_amount
            amount= round(relief_amount,1)
            if amount > 0:
                trans_type = 'ROL'
                self.update_acc_n_bal_record(user_id,new_bal,amount,trans_type)
        
    def account_update(self):
            try:
                all_stakes_in_this_market = Stake.objects.filter(market = self.market).all()#R

                for user_stak in all_stakes_in_this_market: 
                    # user_stake is object to access below
                    # :user_stak.amount                # BET AMOUNT
                    # :user_stak..marketselection.odds # ODDS

                    self.update_winner_losser(user_stak) ###M
    
            # [self.update_winner_losser(user_stak,user_current_account_bal) for _stake in all_stakes_in_this_market for user_stak in all_stakes_of_this_user ]                                                         
                self.closed= True

            except Exception as e:
                print('RESULTACCOUNT:',e)
                return
       
    def update_db_records(self):
        try:
            set_per_return = self.market.per_retun
            self.return_per =set_per_return
            self.gain = self.market.gain_after_relief
            WheelSpin.objects.filter(id = self.market_id).update(receive_results =True) # self.market.update(closed=True) or self.market.closed=True DOESN'T WORK
            
        except Exception as e:
            print('update_db_records ERROR:',e)
            pass

    def save(self, *args, **kwargs):  
        ''' Overrride internal model save method to update balance on staking  '''
        if not self.resu:
            self.resu = self.determine_result_algo

        if  self.resu and not self.closed:
            self.update_db_records()
            self.account_update()

            super().save(*args, **kwargs) #save only if 

        else:
            return


class Istake (TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_wp_istakes',blank =True,null=True)
    marketselection = models.ForeignKey(Selection, on_delete=models.CASCADE,related_name='imarketselections',blank =True,null=True)#
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    stake_placed = models.BooleanField(blank =True,null=True)#
    has_record = models.BooleanField(blank =True,null=True) #
    bet_on_real_account = models.BooleanField(default=False)
    outcome_received= models.BooleanField(default=False)

    def __str__(self):
        return f'Istake:{self.amount} for:{self.user}'

    @property
    def this_user_has_cash_to_bet(self):
        if self.amount> set_up.min_bet: # unti neative values
            if not self.bet_on_real_account:
                try:
                    if current_account_trialbal_of(self.user_id) >=self.amount:
                        return True
                    return False
                except Exception as e:
                    return e    

            else:
                try:
                    if current_account_bal_of(self.user_id) >=self.amount:
                        return True
                    return False
                except Exception as e:
                    return e
        else:
            return False
        

    def deduct_amount_from_this_user_account(self):
        if not self.bet_on_real_account:
            new_bal = current_account_trialbal_of(self.user_id) - float(self.amount)
            update_account_trialbal_of(self.user_id,new_bal)# F3
        else:
            new_bal = current_account_bal_of(self.user_id) - float(self.amount)
            update_account_bal_of(self.user_id,new_bal)# F3
            
    def bet_status(self):
        try:
            return IoutCome.objects.get(stake_id=self.id).win_status
        except  Exception as e:
            print(f'daru_STATUS ERROR:{e}')
            return 'pending'

    @classmethod        
    def spins(cls,user_id):
        return cls.objects.filter(user_id=user_id,outcome_received=false)  


    def save(self, *args, **kwargs):
        ''' Bet could only be registered if
            user got enoug real or trial balance
        '''
        if not self.pk:
            print("CB",self.this_user_has_cash_to_bet) #Debug
            if self.this_user_has_cash_to_bet: #then
                self.deduct_amount_from_this_user_account()
      
                super().save(*args, **kwargs) # create a db record
            else:
                return # no db table record to create!   

         


class CashStore(models.Model):
    give_away =  models.DecimalField(('give_away'), max_digits=12, decimal_places=2, default=0)
    to_keep =  models.DecimalField(('to_keep'), max_digits=12, decimal_places=2, default=0)


class IoutCome(TimeStamp):
    stake  = models.OneToOneField(Istake,on_delete=models.CASCADE,related_name='istakes',blank =True,null= True)
    cashstore =models.ForeignKey(CashStore,on_delete=models.CASCADE,related_name='cashstores',blank =True,null= True)
    inbank = models.DecimalField(('inbank'), max_digits=12, decimal_places=2, default=0)
    outbank = models.DecimalField(('outbank'), max_digits=12, decimal_places=2, default=0)
    result = models.IntegerField(blank =True,null= True)
    pointer = models.IntegerField(blank =True,null= True)
    closed = models.BooleanField(default = False,blank =True,null= True)

    # @classmethod
    # def set_store(cls):
    #     try:
    #        cashstore_,_=CashStore.objects.get_or_create(id =1)
    #        cls.objects.update(cashstore=cashstore_)
    #     except Exception as e:
    #         pass

    @property
    def current_update_give_away(self):
        return float(CashStore.objects.get(id =1).give_away)

    @staticmethod
    def update_give_away(new_bal):
        CashStore.objects.filter(id =1).update(give_away= new_bal)


    def give_away(self):
        try:
            return self.cashstore.give_away
        except Exception as e:
            return e 

    @property
    def real_bet(self):
        try:
            return self.stake.bet_on_real_account
        except :
            pass    

    @property
    def determine_result_algo(self):  # fix this
        # if not self.real_bet:
        #     return randint(1,2)        
        try:
            if self.current_update_give_away >= (3*self.stake.amount):  ##TO IMPLEMENT
                return 1
            return 2 
        except Exception as e:
            return e          


    @staticmethod
    def result_to_segment(results = None, segment=29):
        from random import randint, randrange
        if results is None:
            results = randint(1,2)
        if results ==1:
            return randrange(1,segment,2) # odd no b/w 1 to segment(29)
        else:
            return randrange(2,segment,2) # even no b/w 2 to segment(29)
            
    @property
    def segment(self):
        return self.result_to_segment(results = self.result)# ,segment = 29) from settings

    def update_user_trial_account(self):
        this_user= self.stake.user_id
        current_bal=current_account_trialbal_of(this_user)  #F1
        new_bal = current_bal +float(self.stake.amount*2)
        update_account_trialbal_of(this_user,new_bal) #with new_bal


    def update_user_real_account(self):
        this_user= self.stake.user_id
        current_bal=current_account_bal_of(this_user)  #F1
        new_bal = current_bal +float(self.stake.amount*2) # ard Code odds
        update_account_bal_of(this_user,new_bal) #with new_bal


    def update_give_away_bank(self):

        if self.determine_result_algo == 1:
            current_bal = self.current_update_give_away
            new_bal = current_bal - float(self.stake.amount) 
            print(new_bal)
            self.update_give_away(new_bal)

        else:
            current_bal = self.current_update_give_away
            new_bal = current_bal + float(self.stake.amount)
            print(new_bal)
            self.update_give_away(new_bal)
       
    @property
    def win_status(self):
        if self.result==1:
            return 'win'
        return 'loss' 

    @classmethod    
    def open_for_spin(cls,user_id):
        return cls.objects.filter(user_id=user_id,closed=False)


    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                mstore,_ = CashStore.objects.get_or_create(id =1)
                self.cashstore = mstore
                self.result = self.determine_result_algo
                if self.real_bet:
                    if self.result ==1:
                        self.update_user_real_account()
                    self.update_give_away_bank()
                else:
                    if self.determine_result_algo ==1:
                        self.update_user_trial_account()
                self.pointer = self.segment
   
                super().save(*args, **kwargs)
                
            except Exception as e:
                print(f'IoutCome {e}' )                            


           
class Spin(TimeStamp):
    # outcome  = models.OneToOneField(IoutCome,on_delete=models.CASCADE,related_name='ioutcomes',blank =True,null= True)
    result = models.IntegerField(blank =True,null= True)



def process_spins(user_id):
    unclosed_outcomes=IoutCome.objects.filter(user_id=user_id,closed=False)    
