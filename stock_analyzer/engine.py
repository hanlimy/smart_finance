from info_global import get_now

import pandas as pd
from tabulate import tabulate

from PublicDataReader import Kbland
from bs4 import BeautifulSoup

import quandl
import FinanceDataReader as fdr
import requests


quandl.ApiConfig.api_key = "h4m1wXxBGk62tH6XfeWa"


def make_list_item_from_src(info_comm):
    time_before = get_now('TIME')
    print('-' * 100)
    print('[make_list_item_from_src]-START() <{}>'.format(get_now('TIME')))

    for src in info_comm['list_item_src']:
        print(' > source : {}'.format(src))
        df_index = fdr.StockListing(src)
        df_index.to_csv('{}/df_list_item_{}.csv'.format(info_comm['path_output'], src))

    print('[make_list_item_from_src]-END() <{} | {}>'.format(time_before, get_now('TIME')))


def make_stock_item_code(info_comm):
    time_before = get_now('TIME')
    print('-' * 100)
    print('[make_stock_item_code]-START() <{}>'.format(get_now('TIME')))

    dict_item_code = dict()

    for src in info_comm['list_item_src']:
        print(' > source : {}'.format(src))

        df_index = pd.read_csv('{}/df_list_item_{}.csv'.format(info_comm['path_output'], src), index_col=0)

        list_col_sort_type = ['Stocks']
        print(' > list_col_sort_type :', list_col_sort_type)
        df_index = df_index.sort_values(list_col_sort_type, ascending=False)
        df_index.to_csv('{}/df_list_item_sorted_{}.csv'.format(info_comm['path_output'], src))

        if src in ['KRX']:
            tr_value = 'Code'
        elif src in ['NASDAQ', 'S&P500']:
            tr_value = 'Symbol'
        else:
            continue

        df_item_code = df_index[['Name', tr_value]].set_index('Name', drop=True)
        dict_item_code[src] = df_item_code.T.to_dict('records')[0]

        print(' > dict_item_code[{}]: {}'.format(src, dict_item_code))

    info_comm['dict_item_code'] = dict_item_code

    print('[make_stock_item_code]-END() <{} | {}>'.format(time_before, get_now('TIME')))
    

def crawling_ref(info_comm):
    time_before = get_now('TIME')
    print('-' * 100)
    print('[crawling_ref]-START() <{}>'.format(get_now('TIME')))

    code = '089530'  # 에이티세미콘
    url = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={}".format(code)
    print(' > url : ', url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    req = requests.get(url, headers=headers).content

    # 한글 깨짐 방지 decode
    # soup = BeautifulSoup(req.decode('euc-kr', 'replace'), 'html.parser'))
    soup = BeautifulSoup(req.decode('utf-8', 'replace'), 'html.parser')

    print('-' * 100)
    print(soup.title)
    print(soup.find('title'))
    print(soup.a)
    print(soup.find('a'))

    print('-' * 100)
    print(soup.a.attrs)
    print(soup.a.attrs['href'])

    print('-' * 100)
    print(soup.select_one('title'))
    print(soup.select_one('title').get_text())
    print(soup.select_one('title').string.replace(' ', ''))

    print('-' * 100)
    # # print(soup.find_all('a', attrs={'class': 'cmp-table'}))
    print(soup.select_one('td.line'))  # tag.class > tag.class > tag.class ...
    print(soup.select_one('#contentWrap'))  # id > tag.class ...
    print(soup.select('td[title="지피클럽"]'))  # 'tag[type="value"]' > '

    print('[crawling_ref]-END() <{} | {}>'.format(time_before, get_now('TIME')))


def get_naver_finance_basic(info_comm):
    time_before = get_now('TIME')
    print('-' * 100)
    print('[get_naver_finance_basic]-START() <{}>'.format(get_now('TIME')))

    # list_item_target = list(info_comm['item_code']['KRX'].keys())[:10]

    dict_item_code = info_comm['dict_item_code']
    list_item_target = list(dict_item_code['KRX'].keys())
    print(f'list_item_target : {list_item_target}')

    # list_item_target = ['에이티세미콘']

    df_fin_basic = pd.DataFrame(columns=['code', 'eps', 'bps', 'per', 'area_per', 'pbr', 'cash_ratio', 'owner'])

    for idx, item in enumerate(list_item_target):
        print(f' > item : {item} <{idx+1}/{len(list_item_target)}>')
        code = dict_item_code['KRX'][item]

        url = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={}".format(code)
        req = requests.get(url).content
        soup = BeautifulSoup(req.decode('utf-8', 'replace'), 'html.parser')
        if not len(soup):
            print(f'  >> len(soup) is ZERO')

        text_cond_1 = 'td[class="cmp-table-cell td0301"] > dl > dt > b[class="num"]'
        basic_info_item_1 = soup.select(text_cond_1)
        eps = basic_info_item_1[0].get_text() if len(basic_info_item_1) else None
        bps = basic_info_item_1[1].get_text() if len(basic_info_item_1) else None
        per = basic_info_item_1[2].get_text() if len(basic_info_item_1) else None
        area_per = basic_info_item_1[3].get_text() if len(basic_info_item_1) else None
        pbr = basic_info_item_1[4].get_text() if len(basic_info_item_1) else None
        cash_ratio = basic_info_item_1[5].get_text() if len(basic_info_item_1) else None

        df_fin_basic.loc[item] = [code, eps, bps, per, area_per, pbr, cash_ratio, None]

        df_fin_basic.at[item, 'owner'] = []

        list_stock_owner = ["지피클럽", "더에이치테크", "이재용", "자사주"]
        for text_owner in list_stock_owner:
            text_target = soup.select(f'td[title={text_owner}]')
            if len(text_target):
                print(f'  >> text_target  : ', text_target)
                df_fin_basic.at[item, 'owner'] += [text_owner]

    df_fin_basic.to_csv('{}/df_fin_basic.csv'.format(info_comm['path_output']))

    # tablefmt='fancy_grid', 'psql'
    print(tabulate(df_fin_basic, headers='keys', tablefmt='psql', showindex=True, numalign='right'))

    print('[get_naver_finance_basic]-END() <{} | {}>'.format(time_before, get_now('TIME')))


def get_price_stock(info_comm):
    time_before = get_now('TIME')
    print('-' * 100)
    print('[get_price_stock]-START() <{}>'.format(get_now('TIME')))

    dict_item_code = info_comm['dict_item_code']
    list_item_src = list(dict_item_code.keys())

    for src in list_item_src:
        print(' > source : {}'.format(src))

        df_data_total = None

        list_items = list(dict_item_code[src].keys())

        for idx, item in enumerate(list_items):
            print('  - {:20s} <{}/{}>'.format(item, idx+1, len(list_items)))

            df_data_tmp = None
            if src in ['KRX', 'NASDAQ', 'S&P500']:
                df_data_tmp = fdr.DataReader(
                    dict_item_code[src][item], info_comm['date_start'], info_comm['date_end']
                )
            elif src in ['Material']:
                df_data_tmp = quandl.get(
                    dict_item_code[src][item], trim_start=info_comm['date_start'], trim_end=info_comm['date_end']
                )
            df_data_tmp['Item'] = item
            df_data_total = pd.concat([df_data_total, df_data_tmp], axis=0)

        list_col_info = ['Item']
        list_col_show = list_col_info + [col for col in df_data_total.columns if col not in list_col_info]
        df_data_total = df_data_total[list_col_show]

        list_col_round_3 = ['Change']
        df_data_total[list_col_round_3] = df_data_total[list_col_round_3].applymap("{:.3f}".format)
        df_data_total = df_data_total.reset_index()

        df_data_total.to_csv('{}/df_price_stock_{}.csv'.format(info_comm['path_output'], src))

        print(df_data_total)
        print(' > shape of df_data_total :', df_data_total.shape)
        for col in df_data_total.columns:
            print('  - col :', col)

    print('[get_price_stock]-END() <{} | {}>'.format(time_before, get_now('TIME')))


def filter_price_stock(info_comm):
    time_before = get_now('TIME')
    print('-' * 100)
    print('[filter_price_stock]-START() <{}>'.format(get_now('TIME')))

    col_filter = 'Change'

    for src in info_comm['list_item_src']:
        print(' > source : {}'.format(src))

        df_price = pd.read_csv('{}/df_price_stock_{}.csv'.format(info_comm['path_output'], src), index_col=0)

        df_price_filtered = df_price[(df_price[col_filter] > 0.25) & (df_price[col_filter] < 0.3)]

        print(df_price_filtered)

        df_price_filtered.to_csv('{}/df_price_filtered_{}.csv'.format(info_comm['path_output'], src))


    print('[filter_price_stock]-END() <{} | {}>'.format(time_before, get_now('TIME')))


def get_exchange_rate(info_comm):
    print('[get_exchange_rate]')


def get_kor_pdr():
    time_before = get_now('TIME')
    print('-' * 100)
    print('[get_kor_pdr]-START() <{}>'.format(get_now('TIME')))

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

    print('[get_kor_pdr]-END() <{} | {}>'.format(time_before, get_now('TIME')))


if __name__ == "__main__":

    print('PASS')
    # get_nasdaq_quandl()
    # get_kosdaq_fdr()
    # get_kor_pdr()
