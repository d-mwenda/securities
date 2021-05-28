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
