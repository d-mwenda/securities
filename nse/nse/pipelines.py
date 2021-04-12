# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem

from .models import db_connect, create_table, StockExchangeCompany, StockPrice

class SaveStocksPipeline(object):
    """
    Save scrapped company stock data to database
    """
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        company = StockExchangeCompany()
        price = StockPrice()

        company.name = item["company_name"]
        company.symbol = item["ticker_symbol"]
        price.date = item["date"]
        price.price = item["price"]

        # check if company exists
        existing_company = session.query(StockExchangeCompany).filter_by(name=company.name).first()
        if existing_company is not None:
            price.stockexchangecompany = existing_company
        else:
            price.stockexchangecompany = company
        
        try:
            session.add(price)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()


        return item
