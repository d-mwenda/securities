# -*- coding: utf-8 -*-
import logging
import re
from datetime import date

import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

from nse.items import SEItem


class KwayisiSpider(scrapy.Spider):
    """
    get table of listed companies
    parse data and store into DB - some data is dash (not float/int)
    for each ticker, build the js url
    download the js file
    convert the bytes to str
    strip code to remain with uniform data
    split string into uniform list items
    parse data
    store into db date, price, stock exchange (FK relationship)
    """
    name = 'kwayisi'
    allowed_domains = ['afx.kwayisi.org']
    start_urls = ['http://afx.kwayisi.org/nseke/']

    logger = logging.getLogger("kwayisi")

    def parse(self, response):
        """
        What
        Get all the listed tickers on NSE and crawl their respective historical data.
        How:
        Parse the response by:
        1. taking the second table in the response
        2. selecting the table body of the said table
        3. Select ticker and name of listed company from every row of the table body
        4. load the data into items
        5. return generator calling the method to download historical data for each ticker by:
            a) building the full url of the ticker historical data script
            b) getting the script of the historcal data from the built url
            c) calling method to parse the data from the scripts.
        """

        table = response.css("main .t").getall()[1]
        table_body = Selector(text=table).css("tbody")
        ticker_symbols = [row.css("td a::text").getall() for row in table_body.css("tr")]

        root_url = "https://afx.kwayisi.org/chart/nse/"
        for ticker_symbol in ticker_symbols:
            data_js_url = "".join([root_url, ticker_symbol[0]])
            self.logger.debug(f"Crawling the script at {data_js_url}")
            
            yield response.follow(data_js_url, self.parse_data_from_js, meta={"ticker_symbol": ticker_symbol[0], "company_name": ticker_symbol[1]})
    
    def parse_data_from_js(self, response):
        """
        Parse the Text reponse to get historical data of all the tickers.
        """
        # decode response body to string
        try:
            body = response.body.decode("utf-8")
        except TypeError as t:
            self.logger.error(f"Could not decode response into utf-8. Emiited error: {t}")
            return
        
        # extract the data and price data from script text
        data = body[280:-8].split("],")[:-1]

        # tranform data into date, price pairs
        date_price_pairs = [pair.split(",") for pair in data]
        
        # load items
        for date_price_pair in date_price_pairs:
            item_loader = ItemLoader(item=SEItem())
            item_loader.add_value("ticker_symbol", response.meta["ticker_symbol"])
            item_loader.add_value("company_name", response.meta["company_name"])
            item_loader.add_value("date", date_price_pair[0])
            item_loader.add_value("price", date_price_pair[1])
            yield item_loader.load_item()
