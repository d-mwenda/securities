from .models import Stockexchangecompany
from django.views.generic import DetailView


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
    model = Stockexchangecompany
    context_object_name = "company"
    template_name = "stock_trading/company_stock.html"

    # def get(self, request, *args, **kwargs):
    #     return render(request,, {})
