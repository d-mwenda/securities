"""
Get the latest live data from Nairobi Stock Exhange.
This script is meant to be run as a service so that it
fetches data all the time as long as the server is up
and running.
"""
# pyright: reportMissingImports=false
import time
import logging
from pathlib import Path
import sys

project_root = Path(__file__).parents[2].resolve()
sys.path.insert(0, str(project_root))

from securities_data_acquisition.fetch_latest import execute

# TODO make the logger a module level logger
logger = logging.getLogger("nse_fetch_latest")


if __name__ == "__main__":
    while True:
        execute()
        time.sleep(30)