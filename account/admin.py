from django.contrib import admin
from account.models import (
    Account, Currency, RefCredit, RefCreditTransfer,
    TransactionLog, CashDeposit, CashWithrawal, Curr_Variable, AccountSetting
    )


class AccountSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'curr_unit','min_redeem_refer_credit','auto_approve','withraw_factor')
    list_display_links = ('id',)
    search_fields = ('id',)
    list_editable = ('curr_unit','min_redeem_refer_credit','auto_approve','withraw_factor')


admin.site.register(AccountSetting, AccountSettingAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_id', 'user', 'balance', 'actual_balance','withraw_power',
        'withrawable_balance', 'refer_balance', 'trial_balance',
        'cum_deposit','cum_withraw','active','created_at', 'updated_at')
    list_display_links = ('user_id',)
    search_fields = ('user_id',)
    list_editable = ('active',)


admin.site.register(Account, AccountAdmin)

class Curr_VariableAdmin(admin.ModelAdmin):
    list_display = ('id','name','curr_unit',)
    list_display_links = ('id',)
    search_fields = ('id',)


admin.site.register(Curr_Variable, Curr_VariableAdmin)

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id','common_var','name','rate','amount_equip_to_one_ksh','to_token_rate','created_at','updated_at')
    # list_display_links = ('',)
    search_fields = ('name',)
    list_editable = ('name','rate','amount_equip_to_one_ksh')
    # readonly_fields =()

admin.site.register(Currency,CurrencyAdmin)

class RefCreditAdmin(admin.ModelAdmin):
    list_display = ('user_id','user','amount','credit_from','current_bal','approved','closed', 'has_record','created_at','updated_at')
    list_display_links = ('user_id',)
    search_fields = ('user_id',)
    list_editable = ('approved',)

admin.site.register(RefCredit, RefCreditAdmin)

class RefCreditTransferAdmin(admin.ModelAdmin):
    list_display = ('user_id','user','amount','succided','created_at','updated_at')
    list_display_links = ('user_id',)
    search_fields = ('user_id',)
    # list_editable = ('approved',)

admin.site.register(RefCreditTransfer, RefCreditTransferAdmin)

class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ('id','user','amount','now_bal','trans_type','created_at','updated_at')
    list_display_links = ('user',)
    search_fields = ('user',)
    list_filter =('user','trans_type')


admin.site.register(TransactionLog, TransactionLogAdmin)


class CashDepositAdmin(admin.ModelAdmin):
    list_display = ('user','deposited','status','deposit_type','has_record','amount','current_bal','created_at','updated_at')
    list_display_links = ('amount',)
    search_fields = ('amount',)
    list_filter =('user','deposit_type')
    readonly_fields = ('deposited','has_record','current_bal','created_at','updated_at')


admin.site.register(CashDeposit, CashDepositAdmin)


class CashWithrawalAdmin(admin.ModelAdmin):
    list_display = ('id','user','active','cancelled','approved','withrawned','withraw_status','has_record','amount','user_account','created_at','updated_at')
    list_display_links = ('id',)
    search_fields = ('user',)
    list_filter =('user','approved','cancelled','active')
    readonly_fields =('withrawned','has_record','active','user_account','created_at','updated_at')
    list_editable = ('approved','cancelled')

admin.site.register(CashWithrawal, CashWithrawalAdmin)
