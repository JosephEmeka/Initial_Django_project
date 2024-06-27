from rest_framework import serializers
from .models import Account, Transaction


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'pin', 'account_type']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'Transaction_Type', 'transaction_time', 'transaction_status', 'description']


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many = True)

    class Meta:
        model = Account
        fields = ['account_number', 'first_name', 'last_name', 'balance', 'account_type', 'transactions']

        transactions = serializers.StringRelatedField()

    # account_number = serializers.CharField(max_length = 10)
    # first_name = serializers.CharField(max_length = 255)
    # last_name = serializers.CharField(max_length = 255)
    # balance = serializers.DecimalField(max_digits = 13, decimal_places = 2)
    # account_type = serializers.CharField(max_length = 13)
