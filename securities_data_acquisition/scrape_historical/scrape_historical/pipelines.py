# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# pyright: reportMissingImports = false
import logging

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

from .models import db_connect, create_table, StockExchangeCompany, StockPrice
import sys
# TODO remove the path declaration. Get better way to implememnt  the import
sys.path.append(
    r"C:\Users\Derick\projects\securities\securities_data_acquisition"
    )
from db import Company, HistoricalStockData, SecuritiesExchange, Session
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
        existing_company = session.query(StockExchangeCompany).filter_by(
            name=company.name).first()
        if existing_company is not None:
            price.stockexchangecompany = existing_company
        else:
            price.stockexchangecompany = company

        try:
            session.add(price)
            session.commit()

        except exc.SQLAlchemyError:
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
        company = session.query(Company).filter_by(
            ticker_symbol=item["ticker_symbol"]
        ).first()
        if not company:
            # TODO log this
            return item
        entry = HistoricalStockData(company=company,
                                    date=item["date"],
                                    high_price=item["high_price"],
                                    low_price=item["low_price"],
                                    closing_price=item["closing_price"],
                                    volume=item["volume"],
                                    )
        print(f"company={company.name}, date={item['date']}, "
              f"high_price={item['high_price']}, "
              f"low_price={item['low_price']}, "
              f"closing_price={item['closing_price']}, volume={item['volume']}"
              )

        session.add(entry)

        try:
            session.commit()

        except exc.SQLAlchemyError:
            session.rollback()
            raise

        finally:
            session.close()

        return item


class SaveNSEKEListedPipeline:
    logger = logging.getLogger("SaveNSEKEListedPipeline")

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
        securities_exchange = session.query(SecuritiesExchange).filter_by(
            slug="NSE").first()
        company = Company()

        company.ticker_symbol = item["ticker_symbol"]
        company.name = item["company_name"]
        company.ISIN_CODE = item["ISIN_CODE"]
        company.securities_exchange_id = securities_exchange.id

        session.add(company)
        try:
            session.commit()

        except exc.SQLAlchemyError:
            session.rollback()
            raise

        finally:
            session.close()

        return item
