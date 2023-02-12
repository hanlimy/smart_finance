import pandas as pd
import quandl
import FinanceDataReader as fdr
from PublicDataReader import Kbland

quandl.ApiConfig.api_key = "h4m1wXxBGk62tH6XfeWa"


def make_list_item_from_src(info_comm):
    print('[make_list_item_from_src]')

    for src in info_comm['code_item_stock'].keys():
        print(' > source : {}'.format(src))

        if info_comm['code_item_stock'][src] is not None:
            print('  >> [PASS] item already filled : {}'.format(info_comm['code_item_stock'][src]))
            continue

        df_index = fdr.StockListing(src)
        df_index.to_csv('{}/df_list_item_{}.csv'.format(info_comm['path_output'], src))


def make_code_stock_item(info_comm):
    print('[make_code_stock_item]')

    for src in info_comm['code_item_stock'].keys():
        print('-' * 100 + '\n> source : {}'.format(src))

        df_index = pd.read_csv('{}/df_list_item_{}.csv'.format(info_comm['path_output'], src))

        if src in ['KRX']:
            tr_value = 'Code'
        elif src in ['NASDAQ', 'S&P500']:
            tr_value = 'Symbol'
        else:
            continue

        num_samples = 10
        df_item_code_sample = df_index[['Name', tr_value]].set_index('Name', drop=True).iloc[0:num_samples]
        dict_item_code_sample = df_item_code_sample.T.to_dict('records')[0]

        info_comm['code_item_stock'][src] = dict_item_code_sample
        print(dict_item_code_sample)

    return info_comm


def get_price_stock(info_comm):
    print('[get_price_stock]')

    for src in info_comm['code_item_stock'].keys():
        print('-' * 100 + '\n> source : {}'.format(src))

        df_data_total = None
        for item in info_comm['code_item_stock'][src].keys():
            print('  >> item : {}'.format(item))

            df_data_tmp = None
            if src in ['KRX', 'NASDAQ', 'S&P500']:
                df_data_tmp = fdr.DataReader(
                    info_comm['code_item_stock'][src][item], info_comm['date_start'], info_comm['date_end']
                )
            elif src in ['Material']:
                df_data_tmp = quandl.get(
                    info_comm['code_item_stock'][src][item], trim_start=info_comm['date_start'], trim_end=info_comm['date_end']
                )
            df_data_tmp['Item'] = item
            df_data_total = pd.concat([df_data_total, df_data_tmp], axis=0)
        print(df_data_total)

        list_col = ['Item'] + [col for col in df_data_total.columns if col not in ['Item']]
        print(list_col)

        df_data_total = df_data_total[list_col]
        df_data_total.to_csv('{}/df_price_stock_{}.csv'.format(info_comm['path_output'], src))


def get_exchange_rate(info_comm):
    print('[get_exchange_rate]')


def get_kor_pdr():
    print('[get_kor_pdr]')

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
