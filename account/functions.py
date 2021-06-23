# from account.models import Account

# def current_account_bal_of(user_id): #F2
#     try:
#         return float(Account.objects.get(user_id =user_id).balance)
#     except Exception as e:
#         return e

# def update_account_bal_of(user_id,new_bal): #F3
#     try:
#         if new_bal >= 0:
#             Account.objects.filter(user_id =user_id).update(balance= new_bal)
#         else:
#             log_record(user_id,0,'Account Error') # REMOVE
#     except Exception as e:
#         return e


# def current_account_trialbal_of(user_id): #F2
#     try:
#         return float(Account.objects.get(user_id =user_id).trial_balance)
#     except Exception as e:
#         return e

# def update_account_trialbal_of(user_id, new_bal): #F3
#     try:
#         if new_bal >= 0:
#             Account.objects.filter(user_id =user_id).update(trial_balance=new_bal)
#         else:
#             log_record(user_id,0,'Account Error') # REMOVE
#     except Exception as e:
#         return e

# # Helper functions

# def log_record(user_id,amount,trans_type):# F1
#     TransactionLog.objects.update_or_create(user_id =user_id,amount= amount ,trans_type = trans_type)


# def refer_credit_create(credit_to_user,credit_from_username,amount):
#     try:
#         RefCredit.objects.update_or_create(user = credit_to_user,credit_from = credit_from_username, amount= amount)
#     except Exception as e:
#         print(f'RRR{e}')


# def current_account_cum_depo_of(user_id): #F2
#     try:
#         return float(Account.objects.get(user_id =user_id).cum_deposit)
#     except Exception as e:
#         return e

# def update_account_cum_depo_of(user_id,new_bal): #F3
#     try:
#         if new_bal >= 0:
#             Account.objects.filter(user_id =user_id).update(cum_deposit= new_bal)
#         else:
#             pass
#             # log_record(user_id,0,'Account Error') # REMOVE
#     except Exception as e:
#         return e

# def current_account_cum_withraw_of(user_id): #F2
#     try:
#         return float(Account.objects.get(user_id =user_id).cum_withraw)
#     except Exception as e:
#         return e

# def update_account_cum_withraw_of(user_id,new_bal): #F3
#     try:
#         if new_bal >= 0:
#             Account.objects.filter(user_id =user_id).update(cum_withraw= new_bal)
#         else:
#             pass
#             # log_record(user_id,0,'Account Error') # REMOVE
#     except Exception as e:
#         return e
