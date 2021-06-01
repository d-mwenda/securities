from datetime import timedelta
from django.http.response import HttpResponse, JsonResponse
from django.views.generic.base import View
from django.views.generic import DetailView
from django.shortcuts import render
from django.utils import timezone
from .models import  Company, SecuritiesExchange, HistoricalStockData, LiveStockData


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


class CompanyStockView(DetailView):
    """Process view of a company stock profile"""
    slug_field = "ticker_symbol"
    slug_url_kwarg = "ticker"
    model = Company
    context_object_name = "company"
    template_name = "stock_trading/company_stock.html"

    # def get(self, request, *args, **kwargs):
    #     return render(request,, {})


class CompanyStockAPIView(View):
    
    def get(self, request, *args, **kwargs):
        """Fetch company stock history.

        Args:
            request (HTTPRequest): An object representing a request

        Returns:
            HTTPResponse: HTTP JSON with historical data of the said ticker
        """
        from_date = timezone.now().today() - timedelta(days=30)
        queryset = HistoricalStockData.objects.filter(
            company__ticker_symbol=kwargs.get("ticker"),
            company__securities_exchange__slug=kwargs.get("bourse"),
            company__securities_exchange__country__slug=kwargs.get("country"),
            date__gte=from_date
        ).order_by("-date")
        queryset = queryset.values("date", "closing_price")
        queryset = list(queryset)
        print(queryset)
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
        return JsonResponse({"NSE": "Nairobi Stock Exchange"})