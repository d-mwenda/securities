from django.http.response import HttpResponse, JsonResponse
from django.views.generic.base import View
from django.views.generic import DetailView
from django.shortcuts import render

from .models import  Company, SecuritiesExchange, HistoricalStockData, LiveStockData


class BourseSummaryView(DetailView):
    """[summary]

    Args:
        DetailView ([type]): [description]
    """
    pass


class CompanyStockView(DetailView):
    """Process view of a company stock profile"""
    slug_field = "symbol"
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
        # queryset = CompanyStockHistory.objects.filter(
        #     company_id__ticker_symbol=kwargs.get("ticker"),
        #     stock_exchange_id__slug=kwargs.get("bourse"),
        #     country_id__slug=kwargs.get("country")
        # )
        return JsonResponse({"EQTY": "Equity Bank"})


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