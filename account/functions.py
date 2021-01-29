# from .models import Account,TransactionLog,RefCredit


# def log_record(user_id,amount,trans_type):# F1
#     TransactionLog.objects.update_or_create(user_id =user_id,amount= amount ,trans_type = trans_type)


# def current_account_bal(user_id): #F2
#     try:
#         return float(Account.objects.get(user_id =user_id).balance)
#     except Exception as e:
#         return e  

# def current_account_bal_of(user_id): #F2
#     try:
#         return float(Account.objects.get(user_id =user_id).balance)
#     except Exception as e:
#         return e

# def update_account_bal(user_id,new_bal): #F3
#     try:
#         Account.objects.filter(user_id =user_id).update(balance= new_bal)
#     except Exception as e:
#         return e

# def update_account_bal_of(user_id,new_bal): #F3
#     try:
#         Account.objects.filter(user_id =user_id).update(balance= new_bal)
#     except Exception as e:
#         return e

# def refer_credit_create(credit_to_user,credit_from_username,amount):
#     try:
#         RefCredit.objects.update_or_create(user = credit_to_user,credit_from = credit_from_username, amount= amount)
#     except Exception as e:
#         print(f'RRR{e}')

