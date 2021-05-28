"""Commonly shared utility functions
"""
from datetime import timedelta

def next_trading_day(date_):
    """Return the next trading day.
    It doesn't return weekends by being recursive when necessary.
    As currently implemented, it doesn't recognize holidays of any kind.
    While that's a weakness, at least it accurately identifies at least
    100 non-trading days every year.

    Args:
        date_string (date): a datetime object
    """
    next_day = date_ + timedelta(days=1)
    weekend = ["Saturday", "Sunday"]
    if next_day.strftime("%A") in weekend:
        return next_trading_day(next_day)
    return next_day
