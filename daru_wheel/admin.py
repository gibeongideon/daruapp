from django.contrib import admin
from .models import (
    Stake, WheelSpin, CumulativeGain, Result, Selection, MarketType,
    OutCome, MarketType, Selection, DaruWheelSetting, Istake, IoutCome ,CashStore)


class DaruWheelSettingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'return_val', 'min_redeem_refer_credit',
        'refer_per', 'closed_at', 'results_at','min_bet', 'wheelspin_id',
        'created_at', 'updated_at',)
    list_display_links = ('id',)
    list_editable = (
        'return_val', 'min_redeem_refer_credit', 'refer_per',
        'closed_at', 'results_at','min_bet', 'wheelspin_id',)


admin.site.register(DaruWheelSetting, DaruWheelSettingAdmin) 

class MarketTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'this_market_selection_id_list',
        'this_market_selection_verbose_list', 'created_at', 'updated_at',)

    list_display_links = ('id',)
    # list_editable = ('closed',)


admin.site.register(MarketType, MarketTypeAdmin)


class SelectionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'market_id', 'odds', 'name', 'created_at','updated_at')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('mrtype', 'odds')


admin.site.register(Selection, SelectionAdmin)


class WheelSpinAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'market', 'active', 'receive_results',
        'place_stake_is_active', 'open_at', 'closed_at',
        'results_at', 'updated_at','total_bet_amount_per_marktinstance',
        'selection_bet_amount', 'black_bet_amount', 'white_bet_amount',
        'offset', 'gain_after_relief', 'get_result_active',)

    list_display_links = ('id',)
    readonly_fields = (
        'id', 'market', 'receive_results', 'active',
        'place_stake_is_active', 'open_at', 'closed_at', 'results_at',
        'updated_at', 'total_bet_amount_per_marktinstance',
        'selection_bet_amount', 'black_bet_amount', 'white_bet_amount',
        'offset', 'gain_after_relief', 'place_stake_is_active',
        'get_result_active',)


admin.site.register(WheelSpin, WheelSpinAdmin)


class StakeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'market', 'marketselection', 'current_bal',
        'amount', 'stake_placed', 'has_record',
        'update_account_on_win_lose', 'created_at', 'updated_at')

    list_display_links = ('user',)
    search_fields = ('user',)
    # list_editable = ('outcome',)
    list_filter =('user', 'market', 'marketselection')
    readonly_fields = ('current_bal', 'market')


admin.site.register(Stake, StakeAdmin)


class CumulativeGainAdmin(admin.ModelAdmin):
    list_display = ('id', 'gain', 'gainovertime', 'created_at', 'updated_at')
    list_display_links = ('id',)
    # list_editable = ('',)


admin.site.register(CumulativeGain, CumulativeGainAdmin) 


class OutComeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'market', 'closed', 'result', 'pointer',
        'determine_result_algo', 'segment', 'created_at', 'updated_at')

    list_display_links = ('id',)
    readonly_fields = ('closed', 'result', 'pointer')


admin.site.register(OutCome, OutComeAdmin) 


class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'closed', 'market', 'resu', 'gain',
        'return_per', 'created_at', 'updated_at',)
    list_display_links = ('id',)


admin.site.register(Result, ResultAdmin)




class IstakeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'marketselection',
        'amount', 'bet_on_real_account','this_user_has_cash_to_bet', 'stake_placed', 'has_record',
        'created_at', 'updated_at')

    list_display_links = ('user',)
    search_fields = ('user',)
    list_filter =('user', 'marketselection')



admin.site.register(Istake, IstakeAdmin)


class IoutComeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'stake', 'closed','give_away', 'result', 'pointer',
        'determine_result_algo', 'segment', 'created_at', 'updated_at')

    list_display_links = ('id',)
    readonly_fields = ('closed', 'result', 'pointer')


admin.site.register(IoutCome, IoutComeAdmin)


admin.site.register(CashStore)
 
