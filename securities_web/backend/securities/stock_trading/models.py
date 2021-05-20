from datetime import timedelta

from django.db import models
from django.utils import timezone


class Stockexchangecompany(models.Model):
    name = models.CharField(blank=True, null=True, max_length=100)
    symbol = models.CharField(blank=True, null=True, max_length=4)

    @property
    def year_range(self):
        # Get 52 week range
        time_in_year = timedelta(weeks=52)
        from_date = timezone.now().today() - time_in_year
        qs = self.stock_price(date__gte=from_date)

        # TODO get the highest and lowest and return tuple
        return qs

    @property
    def latest_price(self):
        qs = self.stock_price.all().order_by("-date")[0]
        # TODO: check the last trading day to make sure stock  isn't suspended
        return qs.price

    class Meta:
        managed = False
        db_table = 'stockexchangecompany'


class Stockprice(models.Model):
    company = models.ForeignKey(
        Stockexchangecompany, models.PROTECT,
        blank=True, null=True, related_name="stock_price"
    )
    price = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stockprice'
