from django.db import models
from django.conf import settings
from django.db.models import Sum
from datetime import timedelta
from random import randint
from django.utils import timezone
try:
    from account.models import *
except ImportError:
    pass
from django.contrib.auth import get_user_model
from dashboard.models import TimeStamp
User = get_user_model()

class DaruWheelSetting(TimeStamp):
    return_val = models.FloatField(default=0, blank=True, null=True)
    min_redeem_refer_credit = models.FloatField(default=1000, blank=True, null=True)
    refer_per = models.FloatField(default=0, blank=True, null=True)
    per_to_keep = models.FloatField(default=5, blank=True, null=True)
    closed_at = models.FloatField(help_text='sensitive settings value.Dont edit',default=4.7, blank=True, null=True)
    results_at = models.FloatField(help_text='sensitive settings value.Dont edit',default=4.8, blank=True, null=True)
    wheelspin_id = models.IntegerField(help_text='super critical setting value.DONT EDIT!',default=1, blank=True, null=True)
    curr_unit = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    min_bet = models.DecimalField(max_digits=5,default=45.9, decimal_places=2, blank=True, null=True)
    win_algo = models.IntegerField(default=1,help_text='1=Random win_RECO,2=Using i win rate  Algo,3=Sure win_to_impress_', blank=True, null=True)
    trial_algo = models.IntegerField(
        default=1,
        help_text='1=Normal win_RECO,2=Super win_to_impress,others=Use_win_algo_above',
        blank=True, null=True)
    big_win_multiplier = models.FloatField(default=10, blank=True, null=True)  
    
    class Meta:
        db_table = "d_daruwheel_setup"

    # @classmethod
    # def get_setup(self, cls):
    #     set_up, _=cls.objects.get_or_create(id=1)
    #     return set_up

def wheel_setting():
    set_up, created = DaruWheelSetting.objects.get_or_create(id=1)
    return set_up

class Selection(TimeStamp):
    name = models.CharField(max_length=100, blank=True, null=True)
    odds = models.FloatField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def all_selection(cls):
        return cls.objects.all()

    @classmethod
    def selection_id_list(cls):
        return [_mselect.id for _mselect in cls.objects.all()]

    @classmethod
    def selection_verbose_list(cls):
        return [(_mselect.id, _mselect.name, _mselect.odds) for _mselect in cls.objects.all()]   
  
class WheelSpin(TimeStamp):
    '''Create WheelSpin market instance'''
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
            return Selection.selection_id_list()
        except Exception as e:
            return e    

    def total_bet_amount_per_marktinstance(self):
        try:
            total_amount = Stake.objects.filter(
                market_id=self.id,
                bet_on_real_account=True).aggregate(bet_amount=Sum('amount'))
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
            for selecn in self.market_selection_id_list():
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
        set_up=wheel_setting()
        self.closed_at = self.open_at + timedelta(minutes=set_up.closed_at)
        self.results_at = self.open_at + timedelta(minutes=set_up.results_at)

        if self.active and not self.place_stake_is_active:
            self.active = False  

        super().save(*args, **kwargs)



class Stake (TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_wp_istakes',blank =True,null=True)
    market = models.ForeignKey(WheelSpin, on_delete=models.CASCADE,related_name='market_instnces',blank =True,null=True)
    marketselection = models.ForeignKey(Selection, on_delete=models.CASCADE,related_name='imarketselections',blank =True,null=True)#
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=50)
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
        set_up=wheel_setting()
        if float(self.amount)> set_up.min_bet: # unti neative values
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
                    return 'wind'                    
                return   'losed'
            except  Exception as e:
                print(f'daru_STATUS1 ERROR:{e}')
                return 'pending'                    
        except  Exception as e:
            print(f'daru_STATUS ERROR:{e}')
            return 'pending'

    @classmethod        
    def unspinned(cls,user_id):
        return [obj.id for obj in cls.objects.filter(user=user_id,market=None,spinned=False)]

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

    cumgain = models.ForeignKey("Analytic",on_delete=models.CASCADE,related_name='gains',blank =True,null= True)
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
        return CashStore.objects.get(id =1).give_away

    @staticmethod
    def update_give_away(new_bal):
        CashStore.objects.filter(id =1).update(give_away= new_bal)

    @property
    def current_update_to_keep(self):
        return CashStore.objects.get(id =1).to_keep

    @staticmethod
    def update_to_keep(new_bal):
        CashStore.objects.filter(id =1).update(to_keep= new_bal)

    def user_cum_depo(self):
        pass

    def give_away(self):
        try:
            return self.cashstore.give_away
        except Exception as e:
            return e 

    def real_account_result_algo(self):        
        try:  
            odd= float(self.stake.marketselection.odds)
            stak=float(self.stake.amount)
            set_up=wheel_setting()

            if float(self.current_update_give_away) >= set_up.big_win_multiplier*(stak*odd):
                # print('quolify_4_B-WIN')
                resu=randint(1,5)#properbility_of_winnin_bi
                if resu==1:
                    # print('and_Luck_Strikes!')
                    return 5
                else:#RRR
                    # print('..but_no_luck!')
                    pass                  
                
            if float(self.current_update_give_away) >= (stak*odd):#*self.stake.marketselection.odds):  ##TO IMPLEMENT
                # print('N-Win')
                set_up=wheel_setting()
                # return 1
                if set_up.win_algo ==1:
                    return randint(1,2)

                if set_up.win_algo ==2:
                    resu=randint(1,3)
                    if resu!=1:
                        return 1
                    return 2                   

                if set_up.win_algo ==3:
                    return 1
                else:
                    return 2    
            return 2
        except Exception as e:
            return e 

    def trial_account_result_algo(self):
        set_up=wheel_setting()
        if set_up.trial_algo ==1: # normal win trial
            return randint(1,2)

        elif set_up.trial_algo ==2:# super win trial
            random_val = randint(1,3)
            if random_val == 3:
                return 2
            return 1
        else:
            pass #toREALNormal Win Algo

    def  auto_spin_result_algo(self):
        try:
            B = self.market.selection_bet_amount[0]
            W = self.market.selection_bet_amount[1]            
            # if self.market.place_stake_is_active == False:
            if B == W:
                return randint(1,2) # fix me to get random 1 or 2
            if B > W :
                return 2
            return 1
        except Exception as e:
            print(e)
            return  e

    def  back_store_daruspin_result_algo(self):#TODO#uSE_DIC
        '''
        Winner_deterinin_alotits
        Factors:            
            selection_bet_amount[0]#total_amount_B/total_amount_W
            all_players_B
            all_playesa_W
            current_give_away
            #prefer_site_wit_ore_players_as_lon_as_ie_away _store_allows     

        '''
        try:
            # all_players_B=20
            # all_playesa_W=10
            # total_amount_B=100
            # total_amount_W=80
            # current_give_away=300           


            B = self.market.selection_bet_amount[0]
            W = self.market.selection_bet_amount[1]            
            # if self.market.place_stake_is_active == False:
     
            max_resu=B
            min_resu=W

            bank=self.current_update_give_away

            if bank+min_resu>(max_resu):
                
                # print('top_Players_win')
                return 1                

            elif bank+max_resu>(min_resu):
                # print('low_Players_win')
                return 2

            # else:
            #     return randint(1,2) 
        except Exception as e:
            print(e)
            return  e
            
    @property
    def determine_result_algo(self):  # fix this
        if self.market is None:
            if not self.real_bet:
                return self.trial_account_result_algo()
            else:
                return self.real_account_result_algo() 

        elif self.market:
            # print('YESSSSSS!!!')
            # self.back_store_daruspin_result_algo()#TODO
            # return self.auto_spin_result_algo()
            resu=self.back_store_daruspin_result_algo()
            # print(resu)
            return resu


    @staticmethod
    def result_to_segment(results = None, segment=29):

        from random import randint, randrange
        if results is None:
            # print('Results is NONE')
            results = randint(1,2)
        if results ==1:
            rand_odd= randrange(1,segment,2)          
            if rand_odd==13:
                return 7    
            return rand_odd # odd no b/w 1 to segment(29)
        elif results ==2:
            rand_even= randrange(2,segment,2)          
            if rand_even==28:
                return 16
            return rand_even # even no b/w 2 to segment(29)
        elif results ==5:
            return 13#Bi_win
        elif results ==10:
            return 28#Loose_Turn

        # else:
        #     rand_even= randrange(1,segment,2)          
        #     if rand_even==28:
        #         return 16
        #     return rand_even # even no b/w 2 to segment(29                

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
        try:
            set_up=wheel_setting()
            amount = float(stake_obj.amount)
            odds = float(stake_obj.marketselection.odds)
            per_for_referer = set_up.refer_per  # Settings
            win_amount = (amount *odds)-amount
            if per_for_referer > 100: # Enforce 0<=p<=100 TODO
                per_for_referer = 0

            ref_credit = (per_for_referer/100)*win_amount
            rem_credit = win_amount -ref_credit           
            return win_amount,ref_credit,rem_credit
        except Exception as  e:
            print('update_al_error')
            print(e) 
 
    @property
    def win_status(self):
        if self.market is None:#ispin
            if self.result==1 or self.result==5:
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
            this_user_refercode = this_user.referer_code # first name is used as referer code
            if not this_user_refercode:              
                this_user_refercode =User.objects.get(id=1).code  # settings
            
            referer_users = User.objects.filter(code = this_user_refercode)
            for referer in referer_users:
                refer_credit_create(referer,this_user.username,ref_credit) #F4
                # log_record(referer.id,ref_credit,'ref_credit') # F1 Redundant

        except Exception as e:
            return e#TODO

    def run_update_winner_losser(self,this_user_stak_obj):
        user_id = this_user_stak_obj.user.id
        # user_current_account_bal =current_account_bal_of(user_id)
        # user_current_account_trialbal =current_account_trialbal_of(user_id)

        if this_user_stak_obj.bet_on_real_account==True:#REAL
            if this_user_stak_obj.market is not None:#daru
                if this_user_stak_obj.marketselection_id == self.result:
                    try:
                        win_amount,ref_credit,rem_credit =self.update_values(this_user_stak_obj)
                        trans_type = 'win'
                        all_amount=win_amount+float(this_user_stak_obj.amount)                  
                        self.update_user_real_account(user_id,all_amount)

                        #UUB#Cec
                        current_bal = float(self.current_update_give_away)
                        new_bal = current_bal - win_amount-ref_credit
                        self.update_give_away(new_bal)

                        log_record(user_id,win_amount,trans_type) #F1
                        if ref_credit > 0:
                            trans_type = 'refer-win'
                            self.update_reference_account(user_id,ref_credit,trans_type)

                    except Exception as e:
                        print('EXXXX')
                        print(e)    


                elif this_user_stak_obj.marketselection_id != self.result:
                    pass#TODO

            elif this_user_stak_obj.market is None:#ispin
                win_amount,ref_credit,rem_credit =self.update_values(this_user_stak_obj)
                if self.result ==1:###
                    trans_type='Ispin Win'

                    all_amount=win_amount+float(this_user_stak_obj.amount)
                    self.update_user_real_account(user_id,all_amount)

                    #UUB
                    current_bal = float(self.current_update_give_away)
                    new_bal = current_bal - win_amount-ref_credit
                    self.update_give_away(new_bal)

                    log_record(user_id,win_amount,trans_type) #F1                    
                    if ref_credit > 0:
                        trans_type = 'credit on R Win'
                        self.update_reference_account(user_id,ref_credit,trans_type)


                elif self.result ==2:
                    if ref_credit > 0:
                        trans_type = 'credit on R Loss'

                        self.update_reference_account(user_id,ref_credit,trans_type)
                    #UUB
                    set_up=wheel_setting()
                    current_give_away_bal = float(self.current_update_give_away)
                    current_to_keep_bal = float(self.current_update_to_keep)

                    _to_keep=(float(set_up.per_to_keep)/100)*float(self.stake.amount)
                    _away=float(self.stake.amount)-_to_keep-ref_credit#re

                    away = current_give_away_bal + _away
                    to_keep=current_to_keep_bal+_to_keep
                        
                    self.update_give_away(away)
                    self.update_to_keep(to_keep)

                if self.result ==5:###
                    set_up=wheel_setting()
                    trans_type='Big Win'

                    all_amount=float(win_amount*set_up.big_win_multiplier)+float(this_user_stak_obj.amount)
                    self.update_user_real_account(user_id,all_amount)

                    #UUB
                    sub_amount=all_amount-float(this_user_stak_obj.amount)
                    current_bal = float(self.current_update_give_away)
                    new_bal = current_bal - sub_amount
                    self.update_give_away(new_bal)

                    log_record(user_id,all_amount,trans_type) #F1

        else:#TRIAL
            if this_user_stak_obj.market is not None:#daru
                #WINNER
                if this_user_stak_obj.marketselection_id == self.result:
                    win_amount,ref_credit,rem_credit =self.update_values(this_user_stak_obj)
                    trans_type = 'trial-win'
                    #######
                    self.update_user_trial_account(user_id,rem_credit)
                    log_record(user_id,win_amount,trans_type) #F1
                    # if ref_credit > 0:
                    #     trans_type = 'trial-refer-win'
                    #     self.update_reference_account(user_id,ref_credit,trans_type)
                   
                elif this_user_stak_obj.marketselection_id != self.result:
                    pass
            else:#ispin
                win_amount,ref_credit,rem_credit =self.update_values(this_user_stak_obj)
                if self.result ==1: 
                    all_amount=win_amount+float(this_user_stak_obj.amount)
                    self.update_user_trial_account(user_id,all_amount)

               
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
            try:                
                stake_obj=self.stake
                self.run_update_winner_losser(stake_obj)
            except Exception as e:
                print('IspinACCOUNT:',e)
                return e

       
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
            # if self.market is None :
            mstore,_ = CashStore.objects.get_or_create(id =1)
            self.cashstore = mstore

            if self.market:
                self.update_db_records()#
            try:
                self.result = self.determine_result_algo
                self.pointer = self.segment
                self.run_account_update()
                self.closed= True
                                   
                super().save(*args, **kwargs)                
            except Exception as e:
                print(e)
                return


class Analytic(TimeStamp):
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

