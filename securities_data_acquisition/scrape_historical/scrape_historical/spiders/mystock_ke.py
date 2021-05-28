# -*- coding: utf-8 -*-
import logging
import re
from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

from .utils import next_trading_day
from ..items import MystockKeItem

logger = logging.getLogger("mystock_ke")


class MystocksKeSpider(scrapy.Spider):
    name = "mystocks_ke"
    allowed_domains = ["live.mystocks.co.ke"]
    start_urls = ["http://live.mystocks.co.ke/price_list/20060911"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'scrape_historical.pipelines.SaveMyStocksKePipeline': 300,
        },
        "DOWNLOAD_DELAY" : 5
    }

    def parse(self, response):
        """
        Grab the table with data
        Parse the data into items and load the items.

        Check that the reponse status is 200 before attempting
        to parse.

        Args:
            response ( scrapy HTTP response): typical http response
            but as a scrapy response object.

        Yields:
            1. items to be processed by pipelines
            2. request next url : request-like method that passes the
            response to the passed parser.
        """
        d = re.findall("[0-9]+$", response.url)
        trading_date = datetime.strptime(d[0], "%Y%m%d")

        # verify response OK and parse data
        if response.status == 200:
            s = response.css("#pricelist")
            s = s.css("tr.row").getall()
            s = [BeautifulSoup(x, "html.parser") for x in s]
            for soup in s:
                values = [v for v in soup.stripped_strings]
                if len(values) == 13:
                    # load data into items
                    item_loader = ItemLoader(item=MystockKeItem())
                    item_loader.add_value("ticker_symbol", values[0])
                    item_loader.add_value("date", trading_date)
                    item_loader.add_value("closing_price", values[6])
                    item_loader.add_value("high_price", values[5])
                    item_loader.add_value("low_price", values[4])
                    item_loader.add_value("volume", values[11])
                    print("------------Yielding--------------")
                    i = item_loader.load_item()
                    print(i.keys)
                    yield item_loader.load_item()
            

        # build next url and follow
        next_day = next_trading_day(trading_date)
        next_url = re.sub("[0-9]+$", next_day.strftime("%Y%m%d"), response.url)
        print(next_url)
        yield response.follow(next_url, self.parse)

