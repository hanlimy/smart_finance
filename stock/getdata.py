import pandas as pd
import requests as rq
import FinanceDataReader as fdr

from bs4 import BeautifulSoup


def get_company_code(info_lv2):
    print('-' * 100 + '\n[get_company_code]')

    df_krx = fdr.StockListing('KRX')
    df_krx.to_csv('{}/1-01-01_df_krx.csv'.format(info_lv2['path_output']))
    info_lv2['df_krx'] = df_krx

    df_krx_code = df_krx[['Code', 'Name']].set_index('Name')
    dict_krk_code = df_krx_code.to_dict()['Code']
    info_lv2['dict_company_code'] = dict_krk_code
    print(' > dict_krk_code : {}'.format(dict_krk_code))


def select_target_company(info_lv2):
    print('-' * 100 + '\n[select_target_company]')

    df_krx = info_lv2['df_krx']
    num_com = info_lv2['num_of_target_company']

    col_target = info_lv2['col_target']

    # info_lv2['target_company'] = ['삼성전자', '삼성SDI']
    info_lv2['target_company'] = list(df_krx.sort_values(col_target, ascending=False)['Name'].iloc[0:num_com])
    print(' > target_company : {}'.format(info_lv2['target_company']))


def get_data_naver_stock(info_lv2):
    print('-' * 100 + '\n[get_data_naver_stock]')

    company_code = info_lv2['dict_company_code']
    df_price_all = pd.DataFrame()

    for company_name in info_lv2['target_company']:
        code = company_code[company_name]
        print(' > name : {} | code : {}'.format(company_name, code))

        url = f'https://finance.naver.com/item/sise_day.naver?code={code}'
        headers = {'User-agent': 'Mozilla/5.0'}
        req = rq.get(url, headers=headers)
        html = BeautifulSoup(req.text, 'lxml')

        pgrr = html.find('td', class_='pgRR')
        s = pgrr.a['href'].split('=')
        last_page = int(s[-1])

        page_start = 1
        page_last = page_start + info_lv2['page_cnt']

        df_price = pd.DataFrame()
        for page in range(page_start, page_last):
            print('  >> web page : {} / {}'.format(page, last_page))
            req = rq.get(f'{url}&page={page}', headers=headers)
            df_price = pd.concat([df_price, pd.read_html(req.text, encoding='euc-kr')[0]], ignore_index=True)

        df_price = df_price.dropna().reset_index(drop=True)
        df_price = df_price.rename(columns={
            '날짜': 'date',
            '거래량': 'vol_exch',
            '종가': 'price_end',
            '고가': 'price_high',
            '저가': 'price_low',
        })
        df_price = df_price[['date', 'vol_exch', 'price_end', 'price_high', 'price_low']]
        # df_price_end = df_price[['date', 'vol_exch', 'price_end']]
        # df_price_end = df_price_end.rename(columns={'price_end': 'price_' + name, 'vol_exch': 'vol_' + name})

        df_price.columns = [company_name + '_' + col if col not in ['date'] else col for col in df_price.columns]

        if len(df_price_all):
            df_price_all = pd.merge(df_price_all, df_price, on='date', how='right')
        else:
            df_price_all = df_price

    df_price_all = df_price_all.sort_values('date', ascending=True).reset_index(drop=True)
    df_price_all.to_csv('{}/1-01-99_price_company.csv'.format(info_lv2['path_output']))

    # list_date = list(df_price_all['date'].apply(lambda x: x.split('.')[1] + '/' + x.split('.')[2]))
    #
    # for name in info_lv2['target_company']:
    #     plt.plot(
    #         list_date,
    #         df_price_all['price_' + name]
    #         # label=name
    #     )
    #
    # plt.xticks([list_date[0], list_date[int(len(list_date)/2)], list_date[-1]], rotation=45)
    #
    # plt.legend(loc=(0.05, 0.05))
    # file_name = '{}/price_history.png'.format(info_lv2['path_output'])
    # plt.show(block=False)
    # plt.savefig(file_name)
    # plt.pause(1)
    # plt.close()