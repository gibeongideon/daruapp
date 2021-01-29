from django.db import models
from django.conf import settings
from django.db.models import Sum
from datetime import timedelta,datetime
from random import randint
from django.utils import timezone
try:
    from account.models import RefCredit
    from account.models import update_account_bal_of,current_account_bal_of ,log_record,refer_credit_create
except ImportError as e:
    pass
from django.contrib.auth import get_user_model
User = get_user_model() #make apps independent

set_up ={'return_val':0,'min_redeem_refer_credit':5000,'refer_per':5,'closed_at':4.7,'results_at':4.8,'wheelspin_id':1,'curr_unit':10}


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank =True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank =True,null=True)
    # is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Market(models.Model):
    '''Market place '''
    open_at = models.DateTimeField(default=timezone.now, blank =True,null=True) 
    closed_at = models.DateTimeField(blank =True,null=True)                
    results_at = models.DateTimeField(blank =True,null=True)

    updated_at = models.DateTimeField(auto_now=True,blank =True,null=True)
    active = models.BooleanField(default=True,blank =True,null= True)
    receive_results = models.BooleanField(default=False,blank =True,null= True)

    class Meta:
        abstract = True

    @property
    def place_stake_is_active(self):
        try:
            if timezone.now() >  self.open_at and timezone.now() < self.closed_at:
                return True
            return False
        except Exception as e:
            return e

    @property
    def get_result_active(self):
        try:
            if timezone.now() > self.results_at:# and timezone.now() > self.closed_at:
                return True
            return False
        except Exception as e:
            return e



class MarketType(TimeStamp):
    name = models.CharField(max_length=100,default='M', blank =True,null=True)

    def __str__(self):
        return '{0}:{1}'.format(self.id,self.name)

    def all_selection(self):
        return Selection.objects.filter(mrtype_id = self.id).all()

    def this_market_selection_id_list(self):
        return [_mselect.id for _mselect in self.all_selection() ]

    def this_market_selection_verbose_list(self):
        return [(_mselect.id,_mselect.name,_mselect.odds) for _mselect in self.all_selection()]


class Selection(TimeStamp):
    mrtype = models.ForeignKey(MarketType,on_delete=models.CASCADE,related_name='mrtypes',blank =True,null= True)
    name = models.CharField(max_length=100, blank =True,null=True)
    odds = models.FloatField(max_length=10 ,blank =True,null=True )

    def __str__(self):
        return f'{self.name}'

    def market_id(self):
        return self.mrtype


# class Subselection(TimeStamp):
#     selection = models.ForeignKey(Selection,on_delete=models.CASCADE,related_name='selections',blank =True,null= True)
#     name = models.CharField(max_length=100, blank =True,null=True)
#     odds = models.FloatField(max_length=10 ,blank =True,null=True )

#     def __str__(self):
#         return '{0}SubSelect:{1}'.format(self.selection.name,self.name)

#     def market_id(self):
#         return self.selection


class SettingsVar(TimeStamp):
    return_val = models.FloatField(default = 0,blank =True,null= True)
    min_redeem_refer_credit = models.FloatField(default = 1000,blank =True,null= True)
    refer_per = models.FloatField(default = 0,blank =True,null= True)
    closed_at = models.FloatField(help_text ='sensitive settings value.Dont edit',default =8,blank =True,null= True)
    results_at = models.FloatField(help_text ='sensitive settings value.Dont edit',default =8.1,blank =True,null= True)
    wheelspin_id= models.IntegerField(help_text ='super critical setting value.DONT EDIT!',default=1,blank=True,null=True)
    curr_unit= models.DecimalField(max_digits=6, decimal_places=2,blank=True,null= True)
    
    def save(self, *args, **kwargs):

        set_up['curr_unit'] = self.curr_unit
        set_up['return_val'] = self.return_val
        set_up['min_redeem_refer_credit'] = self.min_redeem_refer_credit
        set_up['refer_per'] = self.refer_per
        set_up['curr_unit'] = self.curr_unit

            
        super().save(*args, **kwargs)


class WheelSpin(Market): 
    market = models.ForeignKey(MarketType,on_delete=models.CASCADE,related_name='wp_markets',blank =True,null= True)   
    # per_relief = models.FloatField(blank =True,null= True)
    per_retun = models.FloatField(default = 0,blank =True,null= True)
    class Meta:
        db_table = "d_wheel_markets"

    def __str__(self):
        return f'WheelSpin No:{self.id}'

    def market_selection_id_list(self):
        return self.market.this_market_selection_id_list()

    def total_bet_amount_per_marktinstance(self):
        try:
            total_amount = Stake.objects.filter(market_id = self.id ).aggregate(bet_amount =Sum('amount'))
            return  total_amount.get('bet_amount')

        except Exception as e:
            return e

    @property
    def black_bet_amount(self):
        try:
            total_amount = Stake.objects.filter(market_id = self.id ).filter(marketselection_id = 1).aggregate(bet_amount =Sum('amount'))
            if total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
            return  0
            
        except Exception as e:
            return e

    @property
    def white_bet_amount(self):

        try:
            total_amount = Stake.objects.filter(market_id = self.id ).filter(marketselection_id = 2).aggregate(bet_amount =Sum('amount'))
            if  total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
            return 0
            
        except Exception as e:
            return e

    def market_stake_amount(self,select_id):

        try:
            total_amount = Stake.objects.filter(market_id = self.id ).filter(marketselection_id = select_id).aggregate(bet_amount =Sum('amount'))
            if  total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
            return 0
        
        except Exception as e:
            return e

    @property
    def selection_bet_amount(self):
        mrkt_bet_amount= []
        for selecn in self.market_selection_id_list():
            mrkt_bet_amount.append(self.market_stake_amount(selecn))

        return mrkt_bet_amount

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
        self.closed_at = self.open_at + timedelta(minutes = set_up['closed_at'])
        self.results_at = self.open_at + timedelta(minutes =set_up['results_at'])

        if self.active and not self.place_stake_is_active:
            self.active = False
        try:
            self.market,_ = MarketType.objects.get_or_create( id= int(set_up['wheelspin_id'] ) )#get_or_create return a tuple/
        except:
            self.market,_ = MarketType.objects.get_or_create( id= 1)
            
        super().save(*args, **kwargs) 

class Stake (TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_wp_stakes',blank =True,null=True)
    market = models.ForeignKey(WheelSpin, on_delete=models.CASCADE,related_name='wheelspins',blank =True,null=True)
    marketselection = models.ForeignKey(Selection, on_delete=models.CASCADE,related_name='marketselections')
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
            market_id = max((obj.id for obj in WheelSpin.objects.all())) #  check if generator can help #ER/empty gen
            this_wheelspin = WheelSpin.objects.get(id =market_id )

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
                        raise Exception ('No cash')
                        # return 'Not enough balance to stake'

                except Exception as e:
                    print('STAKE:',e)
                    return
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
        return self.result_to_segment(results = self.result)# ,segment = 29) fro settings

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
            per_for_referer = set_up['refer_per']  # Settings
            print('REFFC:{per_for_referer}')
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
