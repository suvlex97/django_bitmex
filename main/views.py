import bitmex

from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Account, Order
from .serializers import OrderSerializer
from .permissions import AccountExistPermission


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, AccountExistPermission)
    serializer_class = OrderSerializer

    account = None
    client = None

    def get_account(self) -> Account:
        if self.account is None:
            self.account = Account.objects.prefetch_related('orders').get(name=self.kwargs.get('account_name'))
        return self.account

    # -> SwaggerClient
    def get_client(self):
        if self.client is None:
            account = self.get_account()
            # default test=True. Можна добавити окремим полем в модель Account.
            try:
                self.client = bitmex.bitmex(api_key=account.api_key, api_secret=account.api_secret)
            except Exception:
                raise ValidationError('Failed to connect to BitMEX on account data.')
        return self.client

    def get_queryset(self):
        return self.get_account().orders.all()

    '''
    response exp:
    {
        "orderID": "17bcded9-dfea-4772-b9df-a300ec17dcea",
        "symbol": "XBTUSD",
        "side": "Buy",
        "orderQty": 1,
        "ordType": "Market",
        "price": 50749.5,
        "timestamp": "2021-04-24T19:08:26.394Z",
        ...
    }

    '''

    def perform_create(self, serializer):
        client = self.get_client()
        req_data = self.request.data

        side = req_data['side']
        volume = req_data['volume']
        ord_type = Order.verbose_ord_type_by_id(req_data['ord_type'])
        symbol = req_data['symbol']

        if side == Order.SELL:
            volume = volume * -1

        try:
            resp = client.Order.Order_new(
                symbol=symbol, orderQty=volume, ordType=ord_type
            ).result()
        except Exception as e:
            raise ValidationError(detail=str(e))
        else:
            data = resp.data
            serializer.save(
                order_id=data['orderID'], account=self.get_account(),
                side=side, volume=volume, ord_type=ord_type, symbol=symbol,
                price=data['price'], timestamp=data['timestamp']
            )

    def perform_destroy(self, instance):
        client = self.get_client()
        try:
            resp = client.Order.Order_cancel(
                orderID=self.kwargs.get('pk')
            ).result()
        except Exception as e:
            raise ValidationError(detail=str(e))
        else:
            instance.delete()
