import json
import time
from datetime import datetime
import logging

import requests
from requests.structures import CaseInsensitiveDict

from db import (Session, Company, HistoricalStockData, LiveStockData,
    SecuritiesExchange, Country)

logger = logging.getLogger("nse_fetch_latest")

    # Summarise this file into function calls. Put logic else where
    # call get last data
    # call parse into DB objects
    # call Store live stock data in db
    # call if exchange is closed store close values to historical data (part of above call)
    # 
def nse_fetch():
    """Get the latest stock exchange data from Nairobi Securities
    Exchange in form of JSON.

    Returns:
        requests.Response: an HTTP Response with JSON data.
    """
    url = "https://deveintapps.com/nseticker/api/v1/ticker"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Origin"] = "https://www.nse.co.ke"
    headers["Referrer"] = "https://www.nse.co.ke/"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Connection"] = "keep-alive"
    headers["Content-Length"] = "41"
    headers["Content-Type"] = "application/json"
    headers["DNT"] = "1"
    headers["Host"] = "deveintapps.com"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"

    data = '{"nopage":"true","isinno":"KE3000009674"}'

    resp = requests.post(url, headers=headers, data=data)
    logger.debug(resp.status_code)
    return resp


def parse(response):
    logger.debug("Result of parsing")
    # try or regex ...json errors
    # return formatted dicts in list format
    return json.loads(response)


def market_status(data):
    """Check whether the market is open or closed.

    Args:
        data JSON: return value from the parse method
    """
    return data["message"][1]["updated_at"]["market_status"]


def to_db(data):
    """Push the data to the DB for persistence

    Args:
        data (dict): dictionary from parsing the JSON response of the latest data.
    """
    session = Session()
    dataset = dict()
    tickers = data["message"][0]["snapshot"]
    for ticker in tickers:
        issuer = ticker["issuer"]
        dataset[issuer] = LiveStockData()
        # company = session.query(Company).filter_by(ticker_symbol=issuer).first()

        # if company is not None:
        #     dataset[issuer].company = company
        # else:
                # dataset[issuer].company
        dataset[issuer].company = issuer
        dataset[issuer].date = datetime.today().date(),
        dataset[issuer].time = datetime.now().time(),
        dataset[issuer].price = ticker["price"]
        session.add(dataset[issuer])

    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def execute():
    print("Start...")
    logger.debug(f"{datetime.now().strftime('%d-%m-%Y, %H:%M:%S')} Starting to "
                "fetch latests data from Nairobi Securites Exchange")
    
    response = nse_fetch()
    if response.status_code != 200:
        logger.error(f"{datetime.now().strftime('%d-%m-%Y, %H:%M:%S')} We have an "
                    f"unexpected with Status code: {response.status_code}")
    
    data = parse(response.content)

    # if market_status(data) == "open":
    to_db(data)

    
    print("...end")
    
    logger.debug(f"{datetime.now().strftime('%d-%m-%Y, %H:%M:%S')} Completed fetching "
                "latests data from Nairobi Securites Exchange")
