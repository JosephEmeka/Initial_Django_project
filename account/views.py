from datetime import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Account, Transaction
from .serializers import AccountSerializer, CreateAccountSerializer, DepositWithdrawSerializer, WithdrawSerializer, \
    TransferSerializer
from rest_framework import status

from .validators import validate_pin


# Create your views here.

# viewSet method
class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = CreateAccountSerializer


# class ListAccount(ListCreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = CreateAccountSerializer

# instead of  writing out the below, we can do the above
# def get_queryset(self):
#     return Account.objects.all()
#
# def get_serializer_class(self):
#     return CreateAccountSerializer

# class based views


# class ListAccount(APIView):
# def get(self, request):
#     accounts = Account.objects.all()
#     serializer = AccountSerializer(accounts, many = True)
#     return Response(serializer.data, status = status.HTTP_200_OK)
#
# def post(self, request):
#     serializer = CreateAccountSerializer(data = request.data)
#     serializer.is_valid(raise_exception = True)
#     serializer.save()
#     return Response(serializer.data, status = status.HTTP_201_CREATED)


# function based view
# @api_view(['GET', 'POST'])
# def list_account(request):
#     if request.method == 'GET':
#         accounts = Account.objects.all()
#         serializer = AccountSerializer(accounts, many = True)
#         return Response(serializer.data, status = status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = CreateAccountSerializer(data = request.data)
#         serializer.is_valid(raise_exception = True)
#         serializer.save()
#         return Response(serializer.data, status = status.HTTP_201_CREATED)


# class AccountDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Account.objects.all()
#     serializer_class = CreateAccountSerializer

# # class AccountDetails(APIView):
# def get(self, request, pk):
#     account = get_object_or_404(Account, pk = pk)
#     if request.method == 'GET':
#         # account = Account.objects.get(pk = pk)
#         serializer = AccountSerializer(account)
#         return Response(serializer.data, status = status.HTTP_200_OK)
#
# def put(self, request, pk):
#     account = get_object_or_404(Account, pk = pk)
#     serializer = CreateAccountSerializer(account, data = request.data)
#     serializer.is_valid(raise_exception = True)
#     serializer.save()
#     return Response(serializer.data, status = status.HTTP_200_OK)
#
# def delete(self, request, pk):
#     account = get_object_or_404(Account, pk = pk)
#     account.delete()
#     return Response(status = status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "PUT", "PATCH", "DELETE", ])
# def account_detail(request, pk):
#     account = get_object_or_404(Account, pk = pk)
#     if request.method == 'GET':
#         # account = Account.objects.get(pk = pk)
#         serializer = AccountSerializer(account)
#         return Response(serializer.data, status = status.HTTP_200_OK)
#     elif request.method == "PUT":
#         serializer = CreateAccountSerializer(account, data = request.data)
#         serializer.is_valid(raise_exception = True)
#         serializer.save()
#         return Response(serializer.data, status = status.HTTP_200_OK)
#     elif request.method == "DELETE":
#         account.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)


# @api_view(["POST"])
# def deposit(request):
#     account_number = request.data['account_number']
#     amount = Decimal(request.data['amount'])
#     account = get_object_or_404(Account, pk = account_number)
#     account.balance += Decimal(amount)
#     account.save()
#     Transaction.objects.create(
#         account = account,
#         amount = amount,
#     )
#     return Response(data = {"message": "Transaction Successful"}, status = status.HTTP_200_OK)

# except Account.DoesNotExist:
#     return Response(data:{"message":"account does not exist"}, status = status.HTTP_404_NOT_FOUND)


# @api_view(["PATCH"])
# def withdraw(request):
#     account_number = request.data['account_number']
#     pin = request.data['pin']
#     amount = request.data['amount']
#     account = get_object_or_404(Account, pk = account_number)
#     if pin != account.pin:
#         return Response("Invalid Pin", status = status.HTTP_400_BAD_REQUEST)
#     if account.balance < amount <= 0:
#         return Response("Insufficient Balance", status = status.HTTP_400_BAD_REQUEST)
#     account.balance -= Decimal(amount)
#     account.save()
#     Transaction.objects.create(
#         account = account,
#         amount = amount,
#         Transaction_Type = "DEB"
#     )
#     return Response(data = {"message": "Transaction Successful"}, status = status.HTTP_200_OK)
#

class CreateAccount(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = CreateAccountSerializer


class deposit(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def post(request):
        serializer = DepositWithdrawSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        account_number = request.data['account_number']
        amount = Decimal(request.data['amount'])
        if amount < Decimal(1):
            return Response(data = {'success': False,
                                    'message': 'Invalid Amount',
                                    'request time': datetime.now()}, status = status.HTTP_400_BAD_REQUEST)

        transaction_details = {}
        account = get_object_or_404(Account, pk = account_number)
        balance = account.balance
        balance += amount
        Account.objects.filter(account_number = account_number).update(balance = balance)
        Transaction.objects.create(
            account = account,
            amount = amount
        )

        transaction_details['account_number'] = account_number
        transaction_details['amount'] = amount
        transaction_details['transaction_type'] = 'CREDIT'
        transaction_details['transaction_time'] = datetime.now()
        transaction_details['message'] = 'Transaction Successful'

        # response = {"message": "Transaction Successful", "balance": balance, "time" :datetime.now()}

        return Response(data = transaction_details, status = status.HTTP_200_OK)


class Withdraw(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WithdrawSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        account_number = request.data['account_number']
        pin = request.data['pin']
        validate_pin(pin)
        amount = Decimal(request.data['amount'])
        if Decimal(1) > amount >= Account.balance:
            return Response(data = {'success': False,
                                    'message': 'Invalid Amount',
                                    'request time': datetime.now()}, status = status.HTTP_400_BAD_REQUEST)
        transaction_details = {}
        account = get_object_or_404(Account, pk = account_number)
        balance = account.balance
        balance -= amount
        Account.objects.filter(account_number = account_number).update(balance = balance)
        Transaction.objects.create(
            account = account,
            amount = amount
        )
        transaction_details['message'] = "successful withdrawal"
        transaction_details['account_number'] = account_number
        transaction_details['amount'] = amount
        transaction_details['transaction_type'] = 'DEBIT'
        transaction_details['transaction_time'] = datetime.now()

        # response = {"message": "Transaction Successful", "balance": balance, "time" :datetime.now()}

        return Response(data = transaction_details, status = status.HTTP_200_OK)


class TransferViewSet(ModelViewSet):
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = TransferSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        sender_account = serializer.data['sender_account']
        receiver_account = serializer.data['receiver_account']
        pin = serializer.data['pin']
        validate_pin(pin)
        amount = Decimal(serializer.data['amount'])
        sender_account_from = get_object_or_404(Account, pk = sender_account)
        receiver_account_to = get_object_or_404(Account, pk = receiver_account)
        balance = sender_account_from.balance
        transaction_details = {}
        if balance > amount:
            balance -= amount
        else:
            return Response(data = {"message": "insufficient funds"}, status = status.HTTP_400_BAD_REQUEST)
        try:
            transferred_balance = receiver_account_to.balance + amount
            Account.objects.filter(pk = receiver_account).update(balance = transferred_balance)
        except Account.DoesNotExist:
            return Response(data = {"message": "Transaction Failed"}, status = status.HTTP_400_BAD_REQUEST)
        Transaction.objects.create(
            account = sender_account_from,
            amount = '- ' + str(amount)
        )
        Transaction.objects.create(
            account = receiver_account_to,
            amount = '+ ' + str(amount)
        )
        transaction_details['receiver_account'] = receiver_account
        transaction_details['amount'] = amount
        transaction_details['transaction_type'] = 'TRANSFER'
        transaction_details['transaction_time'] = datetime.now()

        return Response(data = transaction_details, status = status.HTTP_200_OK)


class CheckBalance(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        account = get_object_or_404(Account, user = user.id)
        balance_details = {'account number': account.account_number, 'balance': account.balance}
        message = f'''
        your new balance is
        {account.balance}
        thank you for banking with jaguda'''
        send_mail(subject = "JAGUDA BANK", message = message, from_email = 'noreply@jaguda.com', recipient_list = [f'{user.email}'])
        return Response(data = balance_details, status = status.HTTP_200_OK)


@api_view()
# @login_required
def check_balance(request):
    user = request.user
    account = get_object_or_404(Account, user = user.id)
    balance_details = {'account number': account.account_number, 'balance': Decimal(account.balance)}
    return Response(data = balance_details, status = status.HTTP_200_OK)
