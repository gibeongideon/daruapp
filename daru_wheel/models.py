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
except ImportError:
    pass

from django.contrib.auth import get_user_model
User = get_user_model() # make apps independent


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

def update_account_trialbal_of(user_id, new_bal): #F3
    from account.models import Account
    try:
        if new_bal >= 0:
            Account.objects.filter(user_id =user_id).update(trial_balance=new_bal)
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
    closed_at = models.FloatField(help_text='sensitive settings value.Dont edit',default=4.7, blank=True, null=True)
    results_at = models.FloatField(help_text='sensitive settings value.Dont edit',default=4.8, blank=True, null=True)
    wheelspin_id = models.IntegerField(help_text='super critical setting value.DONT EDIT!',default=1, blank=True, null=True)
    curr_unit = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    min_bet = models.DecimalField(max_digits=5,default=45.9, decimal_places=2, blank=True, null=True)
    win_algo = models.IntegerField(default=2,help_text='1=Random win_RECO,2=Sure win_to_impress_', blank=True, null=True)
    trial_algo = models.IntegerField(
        default=1,
        help_text='1=Normal win_RECO,2=Super win_to_impress,others=Use_win_algo_above',
        blank=True, null=True)
    
    class Meta:
        db_table = "d_daruwheel_setup"

    @classmethod
    def get_setup(self, cls):
        set_up, _=cls.object.get_or_create(id=1)
        return set_up


try:
    ''' remove no such table on make migrations'''
    set_up, created = DaruWheelSetting.objects.get_or_create(id=1)  # fail save
except Exception as me:
    print("MEE", me)
    pass

class Market(models.Model):
    '''Market place wit different market types  '''
    name = models.CharField(max_length=100, blank=True, null=True)
    # class Meta:
    #     abstract = True

    def __str__(self):
        return f'{self.name} market of id {self.id} '.lower()

    def all_selection(self):
        return Selection.objects.filter(mrtype_id=self.id).all()

    def this_market_selection_id_list(self):
        return [_mselect.id for _mselect in self.all_selection() ]

    def this_market_selection_verbose_list(self):
        return [(_mselect.id, _mselect.name, _mselect.odds) for _mselect in self.all_selection()]
        
class Selection(TimeStamp):
    mrtype = models.ForeignKey(
        Market, on_delete=models.CASCADE,
        related_name='mrtypes', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    odds = models.FloatField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def market_id(self):
        return self.mrtype
  
  
class WheelSpin(TimeStamp):
    '''Create WheelSpin market instance'''
    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
        related_name='markets', blank=True, null=True)

    open_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    results_at = models.DateTimeField(blank=True, null=True)
    
    active = models.BooleanField(default=True, blank=True, null=True)
    per_retun = models.FloatField(default=0, blank=True, null=True)
    receive_results = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        db_table = "d_wheel_markets"

    def __str__(self):
        return f'WheelSpin No:{self.id}'
        
    @property
    def place_stake_is_active(self):
        try:
            if timezone.now() > self.open_at and \
                 timezone.now() < self.closed_at:
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
            return self.market.this_market_selection_id_list()
        except Exception as e:
            return e    

    def total_bet_amount_per_marktinstance(self):
        try:
            total_amount = Stake.objects.filter(
                market_id =self.id,
                bet_on_real_account=True ).aggregate(bet_amount=Sum('amount'))
            return total_amount.get('bet_amount')

        except Exception as e:
            return e

    def market_stake_amount(self, select_id):

        try:
            total_amount = Stake.objects.filter(
                market_id=self.id,
                bet_on_real_account=True).filter(
                    marketselection_id=select_id).aggregate(
                        bet_amount=Sum('amount'))

            if total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
            return 0

        except Exception as e:
            return e

    @property
    def selection_bet_amount(self):
        try:
            mrkt_bet_amount = []
            for selecn in self.market.this_market_selection_id_list():
                mrkt_bet_amount.append(self.market_stake_amount(selecn))
            return mrkt_bet_amount
        except Exception as e:
            return e


    @property
    def offset(self):
        try:
            return abs(self.selection_bet_amount[1] - self.selection_bet_amount[0])

        except Exception as e:
            return e

    @property
    def gain_after_relief(self):
        try:
            per_to_return = self.per_retun
            return ((100 - per_to_return)/100)*float(self.offset)
        except Exception as e:
            return e   

    def save(self, *args, **kwargs):
        self.closed_at = self.open_at + timedelta(minutes=set_up.closed_at)
        self.results_at = self.open_at + timedelta(minutes=set_up.results_at)

        if self.active and not self.place_stake_is_active:
            self.active = False

        try:
            market, _ = Market.objects.get_or_create(
                name='spinner')
            self.market = market
            
            super().save(*args, **kwargs)

        except Exception as e:
            print(f'Daru:Market craete Error:{e} ')
            return 

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

class Stake (TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_wp_istakes',blank =True,null=True)
    market = models.ForeignKey(WheelSpin, on_delete=models.CASCADE,related_name='market_instnces',blank =True,null=True)
    marketselection = models.ForeignKey(Selection, on_delete=models.CASCADE,related_name='imarketselections',blank =True,null=True)#
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    current_bal = models.FloatField(max_length=10,default=0 )#R
    stake_placed = models.BooleanField(blank =True,null=True)#
    has_record = models.BooleanField(blank=True,null=True) #
    has_market = models.BooleanField(default=False, blank=True,null=True)
    bet_on_real_account = models.BooleanField(default=False)
    outcome_received = models.BooleanField(default=False, blank=True,null=True)
    spinned = models.BooleanField(default=False, blank=True,null=True)
    # show_user =  models.BooleanField(default=False, blank=True,null=True)

    def __str__(self):
        return f'stake:{self.amount} by:{self.user}'

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
            self.current_bal=new_bal
            update_account_bal_of(self.user_id,new_bal)# F3

    def bet_status(self):
        try:
            try:
                if not self.market:
                    return OutCome.objects.get(stake_id=self.id).win_status
                if  self.marketselection_id== OutCome.objects.get(market_id=self.market.id).result:
                    return 'win'                    
                return   'lose'
            except  Exception as e:
                print(f'daru_STATUS1 ERROR:{e}')
                return 'pending'                    
        except  Exception as e:
            print(f'daru_STATUS ERROR:{e}')
            return 'pending'

    @classmethod        
    def unspinned(cls,user_id):
        return len(cls.objects.filter(user_id=user_id,spinned=False))  

    @property
    def active_spins(self):
        return self.unspinned(self.user.id)
        # pass

    def save(self, *args, **kwargs):
        ''' Bet could only be registered if user got enoug real or trial balance '''
        if not self.pk:
            if self.this_user_has_cash_to_bet: #then
                self.deduct_amount_from_this_user_account() 
                self.stake_placed= True     
                
            else:
                return # no db table record to create!
            try:
                if not self.has_record:
                    log_record(self.user_id,self.amount,'Stake')                    
                    self.has_record = True
            except:
                pass
            if self.market is not None:
                self.has_market =True
            super().save(*args, **kwargs) # create a db record
            
class CashStore(models.Model):
    give_away =  models.DecimalField(('give_away'), max_digits=12, decimal_places=2, default=0)
    to_keep =  models.DecimalField(('to_keep'), max_digits=12, decimal_places=2, default=0)


class OutCome(TimeStamp):
    market  = models.OneToOneField(WheelSpin,on_delete=models.CASCADE,related_name='marketoutcomess',blank =True,null= True)
    stake  = models.OneToOneField(Stake,on_delete=models.CASCADE,related_name='istakes',blank =True,null= True)
    cashstore =models.ForeignKey(CashStore,on_delete=models.CASCADE,related_name='cashstores',blank =True,null= True)
    result = models.IntegerField(blank =True,null= True)
    pointer = models.IntegerField(blank =True,null= True)
    closed = models.BooleanField(default = False,blank =True,null= True)

    cumgain = models.ForeignKey(CumulativeGain,on_delete=models.CASCADE,related_name='gains',blank =True,null= True)
    return_per =models.FloatField(blank =True,null= True)
    gain = models.DecimalField(('gain'), max_digits=100, decimal_places=5,blank =True,null= True)
    active = models.BooleanField(blank =True,null= True)

    @property
    def real_bet(self):
        try:        
            return self.stake.bet_on_real_account
        except :
            return None    
       
    @property
    def current_update_give_away(self):
        return float(CashStore.objects.get(id =1).give_away)

    @staticmethod
    def update_give_away(new_bal):
        CashStore.objects.filter(id =1).update(give_away= new_bal)
    
    def user_cum_depo(self):
        pass

    def give_away(self):
        try:
            return self.cashstore.give_away
        except Exception as e:
            return e 

    def real_account_result_algo(self):        
        try:                
            if self.current_update_give_away >= (3*self.stake.amount):  ##TO IMPLEMENT
                # return 1
                if set_up.win_algo ==1:
                    print('Using REALrandom Algo')
                    return randint(1,2)

                elif set_up.win_algo ==2:
                    print('Using REALsure win Algo')
                    return 1
                else:
                    return 2    
            return 2 
        except Exception as e:
            return e 

    def trial_account_result_algo(self):
        if set_up.trial_algo ==1: # normal win trial
            print('Using Normal_Trial Al 1')
            return randint(1,2)

        elif set_up.trial_algo ==2:# super win trial
            print('Using super_WinTrial Al 2')
            random_val = randint(1,3)
            if random_val == 3:
                return 2
            return 1
        else:
            print('Using REALNormal4Trial Win Algo')
            pass #toREALNormal Win Algo

    @property
    def determine_result_algo(self):  # fix this
        if self.market is None:
            if not self.real_bet:
                self.trial_account_result_algo()
            else:
                self.real_account_result_algo() 

        elif self.market:
            # self.auto_spin_result_algo()
            try:
                B = self.market.selection_bet_amount[0]
                W = self.market.selection_bet_amount[1]            
                # if self.market.place_stake_is_active == False:
                if B == W:
                    print('UsinRandoAl')
                    return randint(1,2) # fix me to get random 1 or 2
                if B > W :
                    return 2
                return 1
            except Exception as e:
                print(e)
                return  e

    @staticmethod
    def result_to_segment(results = None, segment=29):
        from random import randint, randrange
        if results is None:
            # print('Results is NONE')
            results = randint(1,2)
        if results ==1:
            return randrange(1,segment,2) # odd no b/w 1 to segment(29)
        else:
            return randrange(2,segment,2) # even no b/w 2 to segment(29)

    def selection(self):
        if self.stake is not None:
            return self.stake.marketselection.id
        else:
            return None    

    @property
    def segment(self):
        if self.stake is not None:
            stak =self.stake.marketselection.id
            if self.stake.marketselection.id ==2:
                return self.result_to_segment(results = self.result)
            else:
                if self.result==1:
                    return self.result_to_segment(results = 2)
                else:
                    return self.result_to_segment(results = 1)
        else:
            return self.result_to_segment(results = self.result)    

    def update_user_trial_account(self,this_user,add_amount):
        current_bal=current_account_trialbal_of(this_user)  #F1
        new_bal = current_bal +add_amount
        update_account_trialbal_of(this_user,new_bal) #with new_bal

    def update_user_real_account(self,this_user,add_amount):      
        current_bal=current_account_bal_of(this_user)  #F1
        new_bal = current_bal + add_amount# ard Code odds
        update_account_bal_of(this_user,new_bal) #with new_bal

    @staticmethod
    def update_acc_n_bal_record(user_id,new_bal,rem_credit,trans_type):
        try: 
            update_account_bal_of(user_id,new_bal) #F3       
            log_record(user_id,rem_credit,trans_type) #F1
        except Exception as e:
            print('update_acc_n_bal_record ERROR',e)

    @staticmethod        
    def update_values(stake_obj):
        amount = float(stake_obj.amount)
        odds = float(stake_obj.marketselection.odds)
        per_for_referer = set_up.refer_per  # Settings
        win_amount = amount *odds
        if per_for_referer > 100: # Enforce 0<=p<=100 TODO
            per_for_referer = 0

        ref_credit = (per_for_referer/100)*win_amount
        rem_credit = win_amount -ref_credit        
        return win_amount,ref_credit,rem_credit

    def update_give_away_bank(self):
        if self.result== 1:
            current_bal = self.current_update_give_away
            new_bal = current_bal - float(self.stake.amount) 
            self.update_give_away(new_bal)
        else:
            current_bal = self.current_update_give_away
            new_bal = current_bal + float(self.stake.amount)
            self.update_give_away(new_bal)
 
    @property
    def win_status(self):
        if self.market is None:#ispin
            if self.result==1:
                return 'win'
            return 'loss' 
        else:#daru
            pass      

    @classmethod    
    def open_for_spin(cls,user_id):
        return cls.objects.filter(user_id=user_id,closed=False)
#DARU
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
        # print(user_id,ref_credit,trans_type)
        try:
            this_user = User.objects.get(id = user_id)         
            this_user_ReferCode = this_user.daru_code # first name is used as referer code
            if not this_user_ReferCode:              
                this_user_ReferCode =User.objects.get(id=1).my_code  # settings
            
            referer_users = User.objects.filter(my_code = this_user_ReferCode)
            for referer in referer_users:
                # print(referer,'RefererUser')
                refer_credit_create(referer,this_user.username,ref_credit) #F4
                # log_record(referer.id,ref_credit,'ref_credit') # F1 Redundant
        except Exception as e:
            return e#TODO

    def run_update_winner_losser(self,this_user_stak_obj):
        user_id = this_user_stak_obj.user.id
        user_current_account_bal =current_account_bal_of(user_id)
        user_current_account_trialbal =current_account_trialbal_of(user_id)

        if this_user_stak_obj.bet_on_real_account==True:#REAL
            if this_user_stak_obj.market is not None:#daru
                if this_user_stak_obj.marketselection_id == self.result:
                    win_amount,ref_credit,rem_credit =self.update_values(this_user_stak_obj)
                    trans_type = 'win'
                    ###
                    self.update_user_real_account(user_id,rem_credit)
                    log_record(user_id,rem_credit,trans_type) #F1
                    if ref_credit > 0:
                        trans_type = 'refer-win'
                        self.update_reference_account(user_id,ref_credit,trans_type)

                elif this_user_stak_obj.marketselection_id != self.result:
                    pass#TODO

            else:#ispin
                win_amount,ref_credit,rem_credit =self.update_values(this_user_stak_obj)
                if self.result ==1:###
                    # add_amount=float(self.stake.amount*2)
                    self.update_user_real_account(user_id,rem_credit)
                self.update_give_away_bank()           

        else:#TRIAL
            if this_user_stak_obj.market is not None:#daru
                #WINNER
                if this_user_stak_obj.marketselection_id == self.result:
                    win_amount,ref_credit,rem_credit =self.update_values(this_user_stak_obj)
                    trans_type = 'trial-win'
                    #######
                    self.update_user_trial_account(user_id,rem_credit)
                    log_record(user_id,rem_credit,trans_type) #F1
                    # if ref_credit > 0:
                    #     trans_type = 'trial-refer-win'
                    #     self.update_reference_account(user_id,ref_credit,trans_type)
                   
                elif this_user_stak_obj.marketselection_id != self.result:
                    pass
            else:#ispin
                win_amount,ref_credit,rem_credit =self.update_values(this_user_stak_obj)
                if self.result ==1:
                    # add_amount=float(self.stake.amount*2) 
                    self.update_user_trial_account(user_id,rem_credit)

               
    def run_account_update(self):
        if self.market is not None:            
            try:
                all_stakes_in_this_market = Stake.objects.filter(market = self.market).all()#R
                for user_stak in all_stakes_in_this_market:
                    self.run_update_winner_losser(user_stak) ###M                                                    
                # self.closed= True
            except Exception as e:
                print('RESULTACCOUNT:',e)
                return 
        else:
            # self.update_winner_losser(self.stake)
            stake_obj=self.stake
            self.run_update_winner_losser(stake_obj)
       
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
        if not self.pk and not self.closed:
            if self.market is None :
                mstore,_ = CashStore.objects.get_or_create(id =1)
                self.cashstore = mstore
            else:
                self.update_db_records()#
            try:                
                self.result = self.determine_result_algo
                self.pointer = self.segment
                self.run_account_update()
                self.closed= True
                                   
                super().save(*args, **kwargs)                
            except Exception as e:
                return  








                
                    # iplupdate_reference_account
                    # print('akoisNone')                    
                    # all_gain = float(self.market.offset) # FIX
                    # userstake =  float(this_user_stak_obj.amount) 
                    # if self.result == 2:
                    #     all_lose_stake = float(self.market.selection_bet_amount[0])
                    # elif self.result ==1:                                                                                 
                    #    all_lose_stake = float(self.market.selection_bet_amount[1])
                    # per_to_return = float(self.market.per_retun) # 
                    # relief_amount = self.per_return_relief(all_gain,userstake,all_lose_stake,per_to_return)
                    # new_bal = user_current_account_bal + relief_amount
                    # amount= round(relief_amount,1)
                    # if amount > 0:
                    #     trans_type = 'ROL'

                    # self.update_user_real_account(user_id,new_bal)
                    # log_record(user_id,rem_credit,trans_type) #F1

    # @property
    # def real_bet(self):
    #     try:
    #         return self.stake.bet_on_real_account
    #     except :
    #         return None    
       
                
    # def account_update(self):
    #         try:
    #             all_stakes_in_this_market = Stake.objects.filter(market = self.market).all()#R
    #             for user_stak in all_stakes_in_this_market:
    #                 self.update_winner_losser(user_stak) ###M                                                    
    #             self.closed= True
    #         except Exception as e:
    #             print('RESULTACCOUNT:',e)
    #             return

    # @staticmethod
    # def update_acc_n_trialbal_record(user_id,new_bal,rem_credit,trans_type):
    #     try: 
    #         update_account_trialbal_of(user_id,new_bal) #F3       
    #         log_record(user_id,rem_credit,trans_type) #F1
    #     except Exception as e:
    #         print('update_acc_n_trialbal_record ERROR',e)



    # def update_user_account(self):
    #     this_user=self.stake.user
    #     if self.real_bet:
    #         if self.result ==1:
    #             add_amount=float(self.stake.amount*2)
    #             self.update_user_real_account(this_user,add_amount)
    #         self.update_give_away_bank()
    #     else:
    #         if self.result ==1:
    #             add_amount=float(self.stake.amount*2)                
    #             self.update_user_trial_account(this_user,add_amount)


    # def update_winner_losser(self,this_user_stak_obj):
    #     user_id = this_user_stak_obj.user_id
    #     user_current_account_bal =current_account_bal_of(user_id)
    #     user_current_account_trialbal =current_account_trialbal_of(user_id)

    #     #WINNER 
    #     if this_user_stak_obj.marketselection_id == self.result:
    #         win_amount,ref_credit,rem_credit =self.update_values(this_user_stak_obj)            

    #         trans_type = 'WIN' 
    #         if this_user_stak_obj.bet_on_real_account==False:
    #             self.update_user_trial_account(user_id,win_amount)
    #             log_record(user_id,win_amount,trans_type) #F1

    #         elif this_user_stak_obj.bet_on_real_account==True:
    #             self.update_user_real_account(user_id,rem_credit)
    #             log_record(user_id,rem_credit,trans_type) #F1

    #         if ref_credit > 0:
    #             trans_type = 'R-WIN'
    #             self.update_reference_account(user_id,ref_credit,trans_type)

    #     #LOSER4realaccountonly_relief
    #     elif this_user_stak_obj.marketselection_id != self.result:
    #         if self.market is not None:  
    #             print('akoisNone')
    #             all_gain = float(self.market.offset) # FIX
    #             userstake =  float(this_user_stak_obj.amount)
    #             if self.result == 2:
    #                 all_lose_stake = float(self.market.selection_bet_amount[0])
    #             elif self.result ==1:
    #                 all_lose_stake = float(self.market.selection_bet_amount[1])
    #             per_to_return = float(self.market.per_retun) # 
    #             relief_amount = self.per_return_relief(all_gain,userstake,all_lose_stake,per_to_return)
    #             new_bal = user_current_account_bal + relief_amount
    #             amount= round(relief_amount,1)
    #             if amount > 0:
    #                 trans_type = 'ROL'
    #                 # if this_user_stak_obj.bet_on_real_account==False:
    #                 #     self.update_user_trial_account(user_id,rem_credit)
    #                 #     log_record(user_id,win_amount,trans_type) #F1
    #                 if this_user_stak_obj.bet_on_real_account==True:
    #                     self.update_user_real_account(user_id,new_bal)
    #                     log_record(user_id,rem_credit,trans_type) #F1