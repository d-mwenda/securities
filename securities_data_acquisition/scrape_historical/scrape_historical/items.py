# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
from datetime import date
import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def get_date(raw_data):
    """
    Match and extract the date string and convert it to python date.
    """
    date_string = re.findall("[0-9]+\-[0-9]+\-[0-9]+", raw_data)
    return date.fromisoformat(date_string[0])


def convert_to_float(string):
    try:
        return float(string)
    except ValueError:
        return None

def strip_comma(string):
    return re.sub(",", "", string)

class SEItem(scrapy.Item):
    ticker_symbol = scrapy.Field(output_processor=TakeFirst())
    company_name = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(input_processor=MapCompose(get_date), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert_to_float), output_processor=TakeFirst())


class MystockKeItem(scrapy.Item):
    ticker_symbol = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst())
    closing_price = scrapy.Field(input_processor=MapCompose(convert_to_float), output_processor=TakeFirst())
    high_price = scrapy.Field(input_processor=MapCompose(convert_to_float), output_processor=TakeFirst())
    low_price = scrapy.Field(input_processor=MapCompose(convert_to_float), output_processor=TakeFirst())
    volume = scrapy.Field(input_processor=MapCompose(strip_comma, convert_to_float), output_processor=TakeFirst())

class KENSEItem(scrapy.Item):
    @staticmethod
    def process_isin_code(string):
        """Strip the 'ISIN CODE:' part to remain with the actual ISIN code"""
        return string[10:]
    
    @staticmethod
    def process_ticker_symbol(string):
        """Strip the part 'Trading Symbol:' to remain with the actual symbol"""
        return string[15:]
    
    def process_company_name(string):
        """strip the share type part of the name
        for example: in Safaricom PLC Ord 0.05 return Safaricom PLC
        """
        x = re.search("\sOrd", string)
        if x is not None:
            name_ends_at = (x.span()[0])
            return string[0:name_ends_at]
        else:
            return string

    ticker_symbol = scrapy.Field(input_processor=MapCompose(process_ticker_symbol), output_processor=TakeFirst())
    company_name = scrapy.Field(input_processor=MapCompose(process_company_name),output_processor=TakeFirst())
    ISIN_CODE = scrapy.Field(input_processor=MapCompose(process_isin_code), output_processor=TakeFirst())
