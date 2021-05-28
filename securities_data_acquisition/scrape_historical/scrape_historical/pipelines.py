# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# pyright: reportMissingImports = false
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem

from .models import db_connect, create_table, StockExchangeCompany, StockPrice
from db import Company, HistoricalStockData, Session
# from securities_data_acquisition.db import Company, HistoricalStockData, Session

session = Session()

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

class SaveMyStocksKePipeline(object):
    """Save the data loaded into items into the database.
    Only save data for companies already in the database.
    """

    def process_item(self, item, spider):
        """Save the data into the database.

        Args:
            item (Item): Item with data to be saved.
            spider (Spider): spider from which the item was loaded.
        """
        company = session.query(Company).filter_by(ticker_symbol=item["ticker_symbol"]).first()
        if  not company:
            # TODO log this
            return item
        entry = HistoricalStockData(company=company,
                                    date=item["date"],
                                    high_price=item["high_price"],
                                    low_price=item["low_price"],
                                    closing_price=item["closing_price"],
                                    volume=item["volume"],
                                    )
        print(f"company={company.name}, date={item['date']}, high_price={item['high_price']}, "
                f'low_price={item["low_price"]}, closing_price={item["closing_price"]}, volume={item["volume"]}')

        session.add(entry)

        try:
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
