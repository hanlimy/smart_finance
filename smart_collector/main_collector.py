import matplotlib.pyplot as plt


def get_nasdaq_quandl():
    path_output = 'output_data'

    import quandl
    quandl.ApiConfig.api_key = "h4m1wXxBGk62tH6XfeWa"

    date_start = '2021-01-01'
    date_end = '2022-01-13'

    df_gold = quandl.get("LBMA/GOLD", trim_start=date_start, trim_end=date_end)
    df_silver = quandl.get("LBMA/SILVER", trim_start=date_start, trim_end=date_end)
    df_copper = quandl.get("CHRIS/CME_HG10", trim_start=date_start, trim_end=date_end)
    df_oil = quandl.get("OPEC/ORB", trim_start=date_start, trim_end=date_end)

    df_gold.to_csv('{}/df_gold.csv'.format(path_output))
    df_silver.to_csv('{}/df_silver.csv'.format(path_output))
    df_copper.to_csv('{}/df_copper.csv'.format(path_output))
    df_oil.to_csv('{}/df_oil.csv'.format(path_output))


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