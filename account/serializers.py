from rest_framework import serializers
from .models import Account, Transaction


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user', 'account_number', 'pin', 'account_type']


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


class DepositWithdrawSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length = 10)
    amount = serializers.DecimalField(max_digits = 20, decimal_places = 2)


class WithdrawSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length = 10)
    pin = serializers.CharField(max_length = 4)
    amount = serializers.DecimalField(max_digits = 20, decimal_places = 2)


class TransferSerializer(serializers.Serializer):
    # sender_account_number = serializers.CharField(max_length = 10)
    receiver_account_number = serializers.CharField(max_length = 10)
    pin = serializers.CharField(max_length = 4)
    amount = serializers.DecimalField(max_digits = 20, decimal_places = 2)
