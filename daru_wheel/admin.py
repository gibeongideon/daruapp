from django.contrib import admin
from .models import (
    Stake, WheelSpin, CumulativeGain, Selection,
    OutCome, Selection, DaruWheelSetting,
    CashStore, Market, Ispin)

class MarketAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'this_market_selection_id_list',
        'this_market_selection_verbose_list',)
    list_display_links = ('id',)
    # list_editable = ('',)


admin.site.register(Market, MarketAdmin) 
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


class SelectionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'market_id', 'odds', 'name', 'created_at','updated_at')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('mrtype', 'odds')


admin.site.register(Selection, SelectionAdmin)


class WheelSpinAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'market','receive_results','place_stake_is_active', 'open_at', 'closed_at', 'updated_at','total_bet_amount_per_marktinstance',
        'selection_bet_amount',
        'offset', 'gain_after_relief',)

    list_display_links = ('id',)
    readonly_fields = (
        'id', 'updated_at', 'total_bet_amount_per_marktinstance',
        'selection_bet_amount', 
        'offset', 'gain_after_relief',)


admin.site.register(WheelSpin, WheelSpinAdmin)


# class StakeAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'user', 'market', 'marketselection', 'current_bal',
#         'amount', 'stake_placed', 'has_record',
#         'update_account_on_win_lose', 'created_at', 'updated_at')

#     list_display_links = ('user',)
#     search_fields = ('user',)
#     # list_editable = ('outcome',)
#     list_filter =('user', 'market', 'marketselection')
#     readonly_fields = ('current_bal', 'market')


# admin.site.register(Stake, StakeAdmin)


class CumulativeGainAdmin(admin.ModelAdmin):
    list_display = ('id', 'gain', 'gainovertime', 'created_at', 'updated_at')
    list_display_links = ('id',)
    # list_editable = ('',)


admin.site.register(CumulativeGain, CumulativeGainAdmin) 


# class ResultAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'closed', 'market', 'resu', 'gain',
#         'return_per', 'created_at', 'updated_at',)
#     list_display_links = ('id',)


# admin.site.register(Result, ResultAdmin)




class StakeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user','market', 'marketselection',
        'amount', 'bet_on_real_account','this_user_has_cash_to_bet',
        'stake_placed', 'has_record','bet_status','active_spins',
        'created_at', 'updated_at')

    list_display_links = ('user',)
    search_fields = ('user',)
    list_filter =('user', 'marketselection','market','created_at')



admin.site.register(Stake, StakeAdmin)


class OutComeAdmin(admin.ModelAdmin):
    list_display = (
        'id','market', 'stake', 'closed','give_away', 'result', 'pointer',
        'determine_result_algo', 'segment','real_bet', 'created_at', 'updated_at')

    list_display_links = ('id',)
    readonly_fields = ('closed', 'result', 'pointer')


admin.site.register(OutCome, OutComeAdmin)

class CashStoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'give_away', 'to_keep',)

    list_display_links = ('id',)
    # readonly_fields = ('closgive_away',)


admin.site.register(CashStore, CashStoreAdmin)

class IspinAdmin(admin.ModelAdmin):
    list_display = ('id', 'pointer',)

    list_display_links = ('id',)

admin.site.register(Ispin, IspinAdmin)
