import logging

import scrapy
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

from ..items import KENSEItem

logger = logging.getLogger(__name__)

class KenyaNSE(scrapy.Spider):
    """Crawl the companies listed on Nairobi Securities Exchange.
    """
    name = "nse_kenya_listings"
    allowed_domains = ["www.nse.co.ke"]
    start_urls = ["https://www.nse.co.ke/listed-companies/"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'scrape_historical.pipelines.SaveNSEKEListedPipeline': 300,
        }
    }

    def parse(self, response, **kwargs):
        data_section = response.css(
            "#nse_listedcomppage > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)"
        ).getall()[0]
        ticker_divs_selector = scrapy.Selector(text=data_section)
        ticker_divs = ticker_divs_selector.css(".wpb_wrapper").getall()

        ticker_divs = [BeautifulSoup(div, "lxml") for div in ticker_divs]
        print(len(ticker_divs))
        companies = list()
        for ticker in ticker_divs:
            company = [t for t in ticker.stripped_strings]
            if len(company) == 3: companies.append(company)
            print(f"companies found so far {len(companies)}") # debug code
        
        # load items
        for company in companies:
            item_loader = ItemLoader(item=KENSEItem())
            item_loader.add_value("company_name", company[0])
            item_loader.add_value("ticker_symbol", company[1])
            item_loader.add_value("ISIN_CODE", company[2])
            yield item_loader.load_item()
