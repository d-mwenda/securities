from datetime import timedelta

from django.db import models
from django.utils import timezone


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'category'


class Company(models.Model):
    name = models.CharField(max_length=30)
    ticker_symbol = models.CharField(max_length=10)
    isin_code = models.CharField(db_column='ISIN_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    securities_exchange = models.ForeignKey('SecuritiesExchange', models.DO_NOTHING)
    shares_issued = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    profile = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'
    
    @property
    def year_range(self):
        # Get 52 week range
        time_in_year = timedelta(weeks=52)
        from_date = timezone.now().today() - time_in_year
        qs = self.trading_history.filter(date__gte=from_date).values("closing_price")
        prices = [price["closing_price"] for price in qs]
        range_ = (min(prices), max(prices))
        return range_

    @property
    def latest_price(self):
        qs = self.trading_history.all().order_by("-date")[0]
        # TODO: check the last trading day to make sure stock  isn't suspended
        return qs.closing_price
    
    @property
    def market_cap(self):
        """Calculate the market capitalization of a company.
        """
        return self.latest_price * self.shares_issued
    
    @property
    def latest_trading_volume(self):
        """Return the last volume traded.
        """
        qs = self.trading_history.all().order_by("-date")[0]
        # TODO: check the last trading day to make sure stock  isn't suspended
        return int(qs.volume)
    
    @property
    def day_range(self):
        # Get 52 week range
        from_date = timezone.now().today()
        qs = self.intra_day_trading.filter().values("price")
        prices = [price["closing_price"] for price in qs]
        range_ = (min(prices), max(prices))
        return range_
    
    @property
    def price_change(self):
        """Change in price between the last 2 trading days.
        """
        qs = self.trading_history.all().order_by("-date").values("closing_price")[:2]
        last_prices = [price["closing_price"] for price in qs]
        change = round(last_prices[0] - last_prices[1], 2)
        percentage_change = round((change / last_prices[1]) * 100, 2)
        return change, percentage_change


class Country(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'country'


class HistoricalStockData(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, related_name="trading_history")
    date = models.DateField()
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    closing_price = models.FloatField()
    turnover = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historical_stock_data'


class LiveStockData(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, related_name="intra_day_trading")
    date_time = models.DateTimeField()
    price = models.FloatField(blank=True, null=True)
    turnover = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'live_stock_data'


class SecuritiesExchange(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=10)
    timezone = models.CharField(max_length=15, blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    profile = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'securities_exchange'

