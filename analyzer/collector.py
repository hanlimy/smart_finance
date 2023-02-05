import pandas as pd
import quandl
import FinanceDataReader as fdr
from PublicDataReader import Kbland

quandl.ApiConfig.api_key = "h4m1wXxBGk62tH6XfeWa"


def update_info_comm(info_comm):
    print('[update_info_comm]')

    for src in info_comm['box_code'].keys():
        print('-' * 100 + '\n> source : {}'.format(src))

        if info_comm['box_code'][src] is not None:
            print('  >> [PASS] item already filled : {}'.format(info_comm['box_code'][src]))
            continue

        df_index = fdr.StockListing(src)
        df_index.to_csv('{}/df_index_{}.csv'.format(info_comm['path_output'], src))
        df_index = pd.read_csv('{}/df_index_{}.csv'.format(info_comm['path_output'], src))

        if src in ['KRX']:
            tr_value = 'Code'
        elif src in ['NASDAQ', 'S&P500']:
            tr_value = 'Symbol'
        else:
            continue

        num_samples = 10
        df_item_code_sample = df_index[['Name', tr_value]].set_index('Name', drop=True).iloc[0:num_samples]
        dict_item_code_sample = df_item_code_sample.T.to_dict('records')[0]

        info_comm['box_code'][src] = dict_item_code_sample
        print(dict_item_code_sample)

    return info_comm


def get_data_from_src(info_comm):
    print('[get_data_from_src]')

    for src in info_comm['box_code'].keys():
        print('-' * 100 + '\n> source : {}'.format(src))

        df_data_total = None
        for item in info_comm['box_code'][src].keys():
            print('  >> item : {}'.format(item))

            df_data_tmp = None
            if src in ['KRX', 'NASDAQ', 'S&P500']:
                df_data_tmp = fdr.DataReader(info_comm['box_code'][src][item], info_comm['date_start'], info_comm['date_end'])
            elif src in ['Material']:
                df_data_tmp = quandl.get(
                    info_comm['box_code'][src][item], trim_start=info_comm['date_start'], trim_end=info_comm['date_end']
                )
            df_data_tmp['Item'] = item
            df_data_total = pd.concat([df_data_total, df_data_tmp], axis=0)

        print(df_data_total)
        list_col = ['Item'] + [col for col in df_data_total.columns if col not in ['Item']]
        print(list_col)
        df_data_total = df_data_total[list_col]
        df_data_total.to_csv('{}/df_src_{}.csv'.format(info_comm['path_output'], src))


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
