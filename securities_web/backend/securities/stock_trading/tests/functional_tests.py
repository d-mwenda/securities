import unittest
from selenium import webdriver


class CompanyStockView(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        return super().setUp()

    def tearDown(self) -> None:
        # self.browser.quit()
        return super().tearDown()

    def test_page_displays_figures(self):
        # Derick finds the link to free stock exchange information.
        # He wants to see how his favorite stock performed today in the
        # stock exchange
        self.browser.get("http://localhost:8000/stock-trading/nse/EQTY")
        # He notices the page title and header mention Equity Group
        self.assertIn("Equity Group", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("Equity Group", header_text)
        # His figures of interest are: share price, volume,52-week
        # high and low, market cap, day high and low
        # He notices a nice graph that show the ticker activity for the
        # last one week


if __name__ == "__main__":
    unittest.main(warnings="ignore")
