from django.db import models
from model_utils.models import TimeStampedModel


class Account(TimeStampedModel):
    name = models.CharField('Name', max_length=255, null=True, blank=True)
    api_key = models.CharField('API_KEY', max_length=255, db_index=True)
    api_secret = models.CharField('API_SECRET', max_length=255, db_index=True)

    # Можна добавити для визначення типу аккаунта
    # is_test = models.BooleanField(default=True)

    def __str__(self):
        name = self.name
        return name if name else self.id


class Order(models.Model):
    BUY = 1
    SELL = 2

    SIDE_CHOICES = (
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    )

    MARKET = 1
    # (лимитные ордера не реализовывать)
    # LIMIT = 2
    STOP = 3
    # TODO (лимитные ордера не реализовывать)?
    # STOP_LIMIT = 4
    MARKET_IF_TOUCHED = 5
    # TODO (лимитные ордера не реализовывать)?
    # LIMIT_IF_TOUCHED = 6
    PEGGED = 7

    TYPE_CHOICES = (
        (MARKET, 'Market'),
        # (LIMIT, 'Limit'),
        (STOP, 'Stop'),
        # (STOP_LIMIT, 'StopLimit'),
        (MARKET_IF_TOUCHED, 'MarketIfTouched'),
        # (LIMIT_IF_TOUCHED, 'LimitIfTouched'),
        (PEGGED, 'Pegged'),
    )

    # orderID
    order_id = models.CharField('Order id', max_length=255, primary_key=True, db_index=True)
    account = models.ForeignKey(Account, related_name='orders', on_delete=models.SET_NULL, null=True)
    # TODO choices with all variants
    symbol = models.CharField('Symbol', max_length=255, db_index=True)
    # ordType in system
    ord_type = models.PositiveSmallIntegerField('Order type', choices=TYPE_CHOICES)
    side = models.PositiveSmallIntegerField('Side', choices=SIDE_CHOICES)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    # orderQty in system
    volume = models.DecimalField('Volume', max_digits=14, decimal_places=4)
    timestamp = models.DateTimeField('Timestamp')

    class Meta:
        ordering = ('-timestamp',)

    @classmethod
    def verbose_ord_type_by_id(cls, ord_type_id):
        return dict(cls.TYPE_CHOICES)[int(ord_type_id)]
