
# from django.contrib.auth.models import User
from account.models import *
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('user','balance','refer_balance')
        read_only_fields = ('active', 'is_staff')



class TransactionLogSerializer(serializers.ModelSerializer):
    """
    A TransactionLog serializer to return TransactionLog details
    """
    class Meta:
        model = TransactionLog
        #fields = ('__all__')
        fields = ('id','amount','now_bal','trans_type')
