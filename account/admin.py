from django.contrib import admin
from .models import Account


# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'account_type', 'balance', 'account_number']
    list_per_page = 10
    list_display_links = ('first_name',)
    search_fields = ['account_number', 'first_name', 'last_name']
    list_editable = ['last_name', 'account_type']
