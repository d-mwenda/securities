from django.urls import path

from .views import (CompanyStockView, BourseSummaryView, CompanyStockAPIView,
BourseSummaryAPIView)

urlpatterns = [
    path(
        "<country>/<bourse>", BourseSummaryView.as_view(),
        name="bourse_summary"
        ),
    path(
        "<country>/<bourse>/<ticker>", CompanyStockView.as_view(),
        name="company_stock"
        ),
]

api_urlpatterns = [
    path("<country>/<bourse>", BourseSummaryAPIView.as_view(),
        name="company_stock_api"
        ),
    path("<country>/<bourse>/<ticker>", CompanyStockAPIView.as_view(),
        name="company_stock_api"
        ),
]
