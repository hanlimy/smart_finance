import pandas as pd
from tabulate import tabulate

from PublicDataReader import Kbland
from bs4 import BeautifulSoup

import quandl
import FinanceDataReader as fdr
import requests

quandl.ApiConfig.api_key = "h4m1wXxBGk62tH6XfeWa"


def make_list_item_from_src(info_comm):
    print('-' * 100 + '\n[make_list_item_from_src]')

    for src in info_comm['item_code'].keys():
        print(' > source : {}'.format(src))

        if info_comm['item_code'][src] is not None:
            print('  >> [PASS] item already filled : {}'.format(info_comm['item_code'][src]))
            continue

        df_index = fdr.StockListing(src)
        df_index.to_csv('{}/df_list_item_{}.csv'.format(info_comm['path_output'], src))


def make_stock_item_code(info_comm):
    print('-' * 100 + '\n[make_stock_item_code]')

    for src in info_comm['item_code'].keys():
        print('-' * 100 + '\n> source : {}'.format(src))

        df_index = pd.read_csv('{}/df_list_item_{}.csv'.format(info_comm['path_output'], src))

        if src in ['KRX']:
            tr_value = 'Code'
        elif src in ['NASDAQ', 'S&P500']:
            tr_value = 'Symbol'
        else:
            continue

        df_item_code = df_index[['Name', tr_value]].set_index('Name', drop=True)
        dict_item_code = df_item_code.T.to_dict('records')[0]

        info_comm['item_code'][src] = dict_item_code
        print(dict_item_code)

    return info_comm


def crawling_ref():
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


def get_naver_finance_basic(info_comm):
    print('-' * 100 + '\n[get_naver_finance_basic]')
    # list_item_target = list(info_comm['item_code']['KRX'].keys())[:10]
    # list_item_target += ['에이티세미콘']

    list_item_target = list(info_comm['item_code']['KRX'].keys())
    print(f'list_item_target : {list_item_target}')

    df_fin_basic = pd.DataFrame(columns=['code', 'bps', 'per', 'area_per', 'pbr', 'cash_ratio', 'note'])

    for idx, item in enumerate(list_item_target):
        print(f' > item : {item} <{idx}/{len(list_item_target)}>')
        code = info_comm['item_code']['KRX'][item]

        url = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={}".format(code)
        req = requests.get(url).content
        soup = BeautifulSoup(req.decode('utf-8', 'replace'), 'html.parser')
        if not len(soup):
            print(f'  >> len(soup) is ZERO')

        text_cond = 'td[class="cmp-table-cell td0301"] > dl > dt[class="line-left"] > b[class="num"]'
        basic_info_item = soup.select(text_cond)
        bps = basic_info_item[0].get_text() if len(basic_info_item) else None
        per = basic_info_item[1].get_text() if len(basic_info_item) else None
        area_per = basic_info_item[2].get_text() if len(basic_info_item) else None
        pbr = basic_info_item[3].get_text() if len(basic_info_item) else None
        cash_ratio = basic_info_item[4].get_text() if len(basic_info_item) else None

        df_fin_basic.loc[item] = [code, bps, per, area_per, pbr, cash_ratio, None]

        text_target = soup.select('td[title="지피클럽"]')
        if len(text_target):
            print(f'  >> text_target 지피클럽 : ', text_target)
            df_fin_basic.at[item, 'note'] = '지피클럽'

    df_fin_basic.to_csv('{}/df_fin_basic.csv'.format(info_comm['path_output']))

    # tablefmt='fancy_grid', 'psql'
    print(tabulate(df_fin_basic, headers='keys', tablefmt='psql', showindex=True, numalign='right'))


def get_price_stock(info_comm):
    print('-' * 100 + '\n[get_price_stock]')

    for src in info_comm['item_code'].keys():
        print('-' * 100 + '\n> source : {}'.format(src))

        df_data_total = None
        for item in info_comm['item_code'][src].keys():
            print('  >> item : {}'.format(item))

            df_data_tmp = None
            if src in ['KRX', 'NASDAQ', 'S&P500']:
                df_data_tmp = fdr.DataReader(
                    info_comm['item_code'][src][item], info_comm['date_start'], info_comm['date_end']
                )
            elif src in ['Material']:
                df_data_tmp = quandl.get(
                    info_comm['item_code'][src][item], trim_start=info_comm['date_start'], trim_end=info_comm['date_end']
                )
            df_data_tmp['Item'] = item
            df_data_total = pd.concat([df_data_total, df_data_tmp], axis=0)
        print(df_data_total)

        list_col = ['Item'] + [col for col in df_data_total.columns if col not in ['Item']]
        print(list_col)

        df_data_total = df_data_total[list_col]
        df_data_total.to_csv('{}/df_price_stock_{}.csv'.format(info_comm['path_output'], src))


def get_exchange_rate(info_comm):
    print('-' * 100 + '\n[get_exchange_rate]')


def get_kor_pdr():
    print('-' * 100 + '\n[get_kor_pdr]')

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
