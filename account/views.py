from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Account, Transaction
from .serializers import AccountSerializer, CreateAccountSerializer
from rest_framework import status


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


@api_view(["POST"])
def deposit(request):
    account_number = request.data['account_number']
    amount = Decimal(request.data['amount'])
    account = get_object_or_404(Account, pk = account_number)
    account.balance += Decimal(amount)
    account.save()
    Transaction.objects.create(
        account = account,
        amount = amount,
    )
    return Response(data = {"message": "Transaction Successful"}, status = status.HTTP_200_OK)

    # except Account.DoesNotExist:
    #     return Response(data:{"message":"account does not exist"}, status = status.HTTP_404_NOT_FOUND)


@api_view(["PATCH"])
def withdraw(request):
    account_number = request.data['account_number']
    pin = request.data['pin']
    amount = request.data['amount']
    account = get_object_or_404(Account, pk = account_number)
    if pin != account.pin:
        return Response("Invalid Pin", status = status.HTTP_400_BAD_REQUEST)
    if account.balance < amount <= 0:
        return Response("Insufficient Balance", status = status.HTTP_400_BAD_REQUEST)
    account.balance -= Decimal(amount)
    account.save()
    Transaction.objects.create(
        account = account,
        amount = amount,
        Transaction_Type = "DEB"
    )
    return Response(data = {"message": "Transaction Successful"}, status = status.HTTP_200_OK)
