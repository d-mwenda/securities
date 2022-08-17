from datetime import timedelta
from gc import get_objects
from django.http.response import JsonResponse
from django.views.generic.base import View
from django.views.generic import DetailView
from django.utils import timezone
from .models import Company, SecuritiesExchange, HistoricalStockData


class BourseSummaryView(DetailView):
    """Process the request for a securities exchange.

    Args:
        DetailView (Django View): Extends Django's DetailView.
    """
    template_name = "stock_trading/bourse.html"
    slug_field = "slug"
    slug_url_kwarg = "bourse"
    model = SecuritiesExchange
    context_object_name = "securities_exchange"

    def get_title_tag(self, **kwargs):
        """Get the title tag for the html template
        """
        title = {}
        title["title_tag"] = self.get_object().name
        return title

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.get_title_tag())
        return ctx


class CompanyStockView(DetailView):
    """Process view of a company stock profile"""
    slug_field = "ticker_symbol"
    slug_url_kwarg = "ticker"
    model = Company
    context_object_name = "company"
    template_name = "stock_trading/company_stock.html"

    def get_title_tag(self, **kwargs):
        """Get the title tag for the html template
        """
        title = {}
        company = self.get_object()
        title_tag = f"{company.name} {company.securities_exchange.slug} :\
                    {company.ticker_symbol} share price"
        title["title_tag"] = title_tag
        return title

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.get_title_tag())
        return ctx


class CompanyStockAPIView(View):
    """
    Return the stock data for a company in JSON format
    """
    data_periods_mapping = {
        "plot-1-month": 30,
        "plot-3-months": 90,
        "plot-6-months": 180,
        "plot-12-months": 365,
        "plot-5-years": 1825,
        "plot-all": 0,
    }

    def get_from_date(self, data_period):
        """Resolve the date from which to fetch the data.

        Args:
            data_period (string): the data period obtained from the url.
        """
        try:
            days = self.data_periods_mapping[data_period]
        except KeyError:
            days = 30

        from_date = timezone.now().today() - timedelta(days=days)
        return from_date

    def get(self, request, *args, **kwargs):
        """Fetch company stock history.

        Args:
            request (HTTPRequest): An object representing a request

        Returns:
            HTTPResponse: HTTP JSON with historical data of the said ticker
        """
        data_period = kwargs.get("period")

        queryset = HistoricalStockData.objects.filter(
            company__ticker_symbol=kwargs.get("ticker"),
            company__securities_exchange__slug=kwargs.get("bourse"),
            company__securities_exchange__country__slug=kwargs.get("country")
        )
        if data_period != "plot-all":
            from_date = self.get_from_date(data_period)
            queryset = queryset.filter(date__gte=from_date)

        queryset = queryset.order_by("-date")
        queryset = queryset.values("date", "closing_price")
        queryset = list(queryset)
        return JsonResponse(queryset, safe=False)


class BourseSummaryAPIView(View):

    def get(self, request, *args, **kwargs):
        """Process fetching latest Bourse Summary.

        Args:
            request (HttpRequest): An object representing an HTTP Request.
        """
        queryset = SecuritiesExchange.objects.filter(
            stock_exchange_id__slug=kwargs.get("bourse"),
            country_id__slug=kwargs.get("country")
        )
        return JsonResponse(queryset)
