from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer, CreateAccountSerializer
from rest_framework import status


# Create your views here.

@api_view(['GET', 'POST'])
def list_account(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CreateAccountSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)


@api_view()
def account_detail(request, pk):
    account = get_object_or_404(Account, pk = pk)
    # account = Account.objects.get(pk = pk)
    serializer = AccountSerializer(account)
    return Response(serializer.data, status = status.HTTP_200_OK)
    # except Account.DoesNotExist:
    #     return Response(data:{"message":"account does not exist"}, status = status.HTTP_404_NOT_FOUND)
