from rest_framework import serializers
from .models import Account


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'pin', 'account_type']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_number', 'first_name', 'last_name', 'balance', 'account_type']

    # account_number = serializers.CharField(max_length = 10)
    # first_name = serializers.CharField(max_length = 255)
    # last_name = serializers.CharField(max_length = 255)
    # balance = serializers.DecimalField(max_digits = 13, decimal_places = 2)
    # account_type = serializers.CharField(max_length = 13)
