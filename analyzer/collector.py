def get_nasdaq_quandl(info_comm):
    print('[get_nasdaq_quandl]')

    import quandl
    quandl.ApiConfig.api_key = "h4m1wXxBGk62tH6XfeWa"

    for key in info_comm['src_nasdaq'].keys():
        print(' > src in nasdaq : ', key)

        df_data = quandl.get(
            info_comm['src_nasdaq'][key], trim_start=info_comm['date_start'], trim_end=info_comm['date_end']
        )

        df_data.to_csv('{}/df_src_nasdaq_{}.csv'.format(info_comm['path_output'], key))


def get_kosdaq_fdr():
    print('[get_kosdaq_fdr]')
    # import FinanceDataReader as fdr

    # df_krx = fdr.StockListing('KRX')
    # df_`appl = fdr.DataReader('AAPL', '2020-01-01', '2020-01-30')


def get_kor_pdr():
    print('[get_kor_pdr]')

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


if __name__ == "__main__":

    print('PASS')
    # get_nasdaq_quandl()
    # get_kosdaq_fdr()
    # get_kor_pdr()
