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


class Country(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'country'


class HistoricalStockData(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, models.DO_NOTHING)
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

