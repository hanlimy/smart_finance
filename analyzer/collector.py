import pandas as pd
import quandl
import FinanceDataReader as fdr
from PublicDataReader import Kbland

quandl.ApiConfig.api_key = "h4m1wXxBGk62tH6XfeWa"


def get_data_from_src(info_comm):
    print('[get_data_from_src]')

    for idx in info_comm['index_stock']:
        print(' > index_stock : {}'. format(idx))
        df_idx = fdr.StockListing(idx)
        df_idx.to_csv('{}/df_idx_{}.csv'.format(info_comm['path_output'], idx))

    idx = 'KRX'
    df_item_code = pd.read_csv('{}/df_idx_{}.csv'.format(info_comm['path_output'], idx))
    df_item_code_sample = df_item_code[['Code', 'Name']].set_index('Name', drop=True).iloc[0:10]
    dict_item_code_sample = df_item_code_sample.T.to_dict('records')[0]
    info_comm['src_kosdaq'] = dict_item_code_sample
    print(dict_item_code_sample)

    list_source = [src for src in info_comm.keys() if 'src' in src]
    for src in list_source:
        print(' > src : {}'.format(src))
        for item in info_comm[src]:
            print('  >> item : {}'.format(item))
            df_data = None
            if src in ['src_material']:
                df_data = quandl.get(
                    info_comm[src][item], trim_start=info_comm['date_start'], trim_end=info_comm['date_end']
                )
            elif src in ['src_kosdaq', 'src_nasdaq']:
                df_data = fdr.DataReader(info_comm[src][item], info_comm['date_start'], info_comm['date_end'])

            df_data.to_csv('{}/df_{}_{}.csv'.format(info_comm['path_output'], src, item))


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
