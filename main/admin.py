from django.contrib import admin

from .models import Account, Order


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = [
        'id', 'name', 'api_key', 'api_secret'
    ]
    search_fields = ('id', 'name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = [
        'order_id', 'account', 'symbol', 'ord_type', 'side', 'price', 'volume', 'timestamp'
    ]
    search_fields = ('order_id', 'account')
    list_filter = ('side',)
