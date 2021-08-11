from datetime import timedelta, datetime

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
        ordering = ["name"]


class Company(models.Model):
    name = models.CharField(max_length=30)
    ticker_symbol = models.CharField(max_length=10)
    isin_code = models.CharField(db_column='ISIN_CODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    securities_exchange = models.ForeignKey('SecuritiesExchange', models.DO_NOTHING, related_name="companies")
    shares_issued = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True, related_name="companies")
    profile = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "company"
        ordering = ["category"]
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def year_range(self):
        # Get 52 week range
        try:
            time_in_year = timedelta(weeks=52)
            from_date = timezone.now().today() - time_in_year
            qs = self.trading_history.filter(date__gte=from_date).values("closing_price")
            prices = [price["closing_price"] for price in qs]
            range_ = (min(prices), max(prices))
            return range_
        except IndexError:
            # TODO Log as error
            return None

    @property
    def latest_price(self):
        try:
            qs = self.trading_history.all().order_by("-date")[0]
            # TODO: check the last trading day to make sure stock  isn't suspended
            return qs.closing_price
        except IndexError:
            # TODO Log as error
            return None
    
    @property
    def market_cap(self):
        """Calculate the market capitalization of a company.
        """
        try:
            return self.latest_price * self.shares_issued
        except:
            return None
    
    @property
    def latest_trading_volume(self):
        """Return the last volume traded.
        """
        try:
            qs = self.trading_history.all().order_by("-date")[0]
            # TODO: check the last trading day to make sure stock  isn't suspended
            return int(qs.volume)
        except IndexError:
            # TODO Log as error
            return None

    @property
    def price_change(self):
        """Change in price between the last 2 trading days.
        """
        try:
            qs = self.trading_history.all().order_by("-date").values("closing_price")[:2]
            last_prices = [price["closing_price"] for price in qs]
            change = round(last_prices[0] - last_prices[1], 2)
            percentage_change = round((change / last_prices[1]) * 100, 2)
            return change, percentage_change
        except IndexError:
            # TODO Log as error
            return None
    
    @property
    def day_range(self):
        # Get day range
        from_date = timezone.now().today()
        # TODO filter date
        if self.last_trading_day() is None:
            return None
        print(f"This stock was last traded on {self.last_trading_day()}")
        qs = self.intra_day_trading.filter(date_time__gt=self.last_trading_day()).values("price")
        print(bool(qs))
        for q in qs:
            print(q)
        prices = [price["price"] for price in qs]
        range_ = (min(prices, default=0), max(prices, default=0))
        return range_
    
    @property
    def day_high(self, day=None):
        """Get the highest price a stock traded during a certain day.

        Args:
            day (date, optional): the datetime object for the day for
            which to evaluate the highest price. Defaults to None.
            If None, get the highest price for the latest available day.

        Returns:
            float: value for the highest price
            None if data is unavailable
        """
        trading_day = day or self.last_trading_day
        qs = self.intra_day_trading.filter(day_time__gte=trading_day)
        
        return price

    # @property
    def last_trading_day(self, day_time=None):
        """Get the last day when a stock was traded.

        Args:
            day_time (datetime, optional):  Defaults to None.

        Returns:
            datetime: Datetime object of the last day the company's stock
            was traded.
        """
        # TODO make it timezone aware
        if day_time is None:
            today = timezone.now().date()
            day_time = timezone.datetime(today.year, today.month, today.day)
        qs = self.intra_day_trading.filter(date_time__gte=day_time)
        if qs.count() < 1:
            try:
                day_time -= timedelta(days=1)
                self.last_trading_day(day_time=day_time)
            except RecursionError:
                return None
        return day_time
    
    @property
    def day_high(self):
        pass

    @property
    def day_low(self, day=None):
        """Get the lowest price a stock traded during a certain day.

        Args:
            day (date, optional): The day for which to evaluate the
            lowest price. Defaults to None. If None, get the lowest
            for the latest available day.

        Returns:
            float: lowest price
            None if data is unavailable
        """
        pass

    @property
    def dividend(self, fiscal_period=None):
        """Get the latest dividend, for when and kind of financial period.

        Args:
            fiescal period (optional): Period for which to to get the dividend.
            If None, get the lastest. 
        Returns:
            dict: dictionary of amount, which fiscal period e.g. 2021 and
            kind of fiscal period e.g. half year or final annual.
        """
        pass

    def dividend_yield(self):
        pass

    def divident_ratio(self):
        pass

    def retention_ratio(self):
        pass


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
        db_table = "securities_exchange"

    def price_changes(self):
        price_changes = []
        companies = self.companies.all()
        for company in companies:
            if company.price_change is not None:
                price_changes.append((company ,company.price_change))
        return sorted(price_changes, key=lambda item: item[1][1],
        reverse=True)

    @property
    def gainers(self):
        """Calculate the top 5  companies with the highest positive percentage
        percentage change in price between the last 2 trading days.
        """
        gainers = self.price_changes()[:5]
        for gainer in gainers:
            if gainer[1][0] < 0: gainers.remove(gainer)
        return gainers

    @property
    def losers(self):
        """Calculate the top 5  companies with the highest negative percentage
        percentage change in price between the last 2 trading days.
        """
        losers = self.price_changes()[-5:]
        for loser in losers:
            if loser[1][0] > 0 : losers.remove(loser)
        losers = [(loser[0], (abs(loser[1][0]), abs(loser[1][1]))) for loser in losers]
        losers = sorted(losers, key=lambda x:x[1][1], reverse=True)
        return losers

    @property
    def movers(self):
        """Calculate the top 5 companies with the highest volume of traded
        shares on the last trading day.
        """
        volumes = []
        companies = self.companies.all()
        for company in companies:
            if company.latest_trading_volume is not None:
                volumes.append(company)
        return sorted(volumes,
                        key=lambda company:company.latest_trading_volume,
                        reverse=True)[:5]
