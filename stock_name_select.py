import FinanceDataReader as fdr
import pandas as pd
import numpy as np
from pykrx import stock

from datetime import datetime

today_date = str(datetime.today()).split(" ")[0].replace("-",'')
name = stock.get_market_ticker_name('005930')
