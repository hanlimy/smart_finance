import pandas as pd
import numpy as np
import random

seed = 42
np.random.seed(seed)
random.seed(seed)


def get_nasdaq_quandl():
    path_output = 'output_data'

    import quandl
    quandl.ApiConfig.api_key = "h4m1wXxBGk62tH6XfeWa"

    date_start = '2022-01-01'
    date_end = '2022-12-31'

    dict_src_nasdaq = {
        'gold': 'LBMA/GOLD',
        'silver': 'LBMA/SILVER',
        'copper': 'CHRIS/CME_HG10',
        'oil': 'OPEC/ORB',
    }

    for key in dict_src_nasdaq.keys():
        print('key :', key)

        df_data = quandl.get(dict_src_nasdaq[key], trim_start=date_start, trim_end=date_end)
        df_data.to_csv('{}/df_{}.csv'.format(path_output, key))


def get_kosdaq_fdr():
    import FinanceDataReader as fdr

    df_krx = fdr.StockListing('KRX')
    df_appl = fdr.DataReader('AAPL', '2020-01-01', '2020-01-30')


def get_kor_pdr():
    from PublicDataReader import Kbland

    api = Kbland()
    params = {
        "월간주간구분코드": "01",
        "매물종별구분": "01",
        "매매전세코드": "01",
        # "지역코드": "11",
        "기간": 1,
    }
    df = api.get_price_index(**params)
    print(df.tail())


get_nasdaq_quandl()