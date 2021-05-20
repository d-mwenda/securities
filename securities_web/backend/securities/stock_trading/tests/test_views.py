"""
Tests for the views of the share_trading app
"""
from django import test
from django.urls import resolve, reverse_lazy
from django.utils import timezone

from stock_trading.models import Stockexchangecompany, Stockprice


class TestBourseSummary(test.TestCase):

    def test_url(self):
        """Test the URL resolves to BourseSummary  view."""
        resolved_to = resolve("/stock-trading/kenya/nse")
        reversed_to = reverse_lazy(
            "bourse_summary",
            kwargs={"country": "kenya", "bourse": "nse"}
            )
        self.assertEqual(resolved_to.view_name, "bourse_summary")
        self.assertEqual(resolved_to.func.__name__, "BourseSummaryView")
        self.assertEqual(reversed_to, "/stock-trading/kenya/nse")


class TestCompanyStock(test.TestCase):

    def setUp(self) -> None:
        eqty = Stockexchangecompany.objects.create(
            name="Equity Group Holdings LTD",
            symbol="EQTY"
        )
        Stockprice.objects.create(
            company=eqty, price="45.6", date=timezone.now().date()
        )
        self.response = self.client.get("/stock-trading/kenya/nse/EQTY")
        return super().setUp()

    def test_url(self):
        """Test the URL resolves to CompanyStock view."""
        resolved_to = resolve("/stock-trading/kenya/nse/EQTY")
        reversed_to = reverse_lazy("company_stock", kwargs={
                        "country": "kenya", "bourse": "nse", "ticker": "EQTY"
                        })
        self.assertEqual(resolved_to.view_name, "company_stock")
        self.assertEqual(resolved_to.func.__name__, "CompanyStockView")
        self.assertEqual(reversed_to, "/stock-trading/kenya/nse/EQTY")

    def test_template_used(self):
        self.assertTemplateUsed(self.response,
                                "stock_trading/company_stock.html")

    def test_context(self):
        self.assertIn("company", self.response.context)
