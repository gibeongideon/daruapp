from django.contrib import admin
from .models import (
    Stake, WheelSpin, CumulativeGain, Result, Selection, MarketType, OutCome)


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
