from django.urls import path

from .views import CompanyStockView, BourseSummaryView

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
