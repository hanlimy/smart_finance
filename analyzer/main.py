from collector import \
    make_list_item_from_src, make_stock_item_code, \
    get_price_stock, get_naver_finance_basic
from visual import make_page
from datetime import datetime


def main():

    today = datetime.now().strftime('%Y-%m-%d')

    info_comm = {

        'date_start': '2022-01-01',
        'date_end': today,
        'path_output': 'output_data',

        'item_code': {
            'KRX': None,
            # 'NASDAQ': None,
            # 'S&P500': None,
        },
    }

    # make_list_item_from_src(info_comm)
    info_comm = make_stock_item_code(info_comm)
    get_naver_finance_basic(info_comm)

    # get_price_stock(info_comm)
    # make_page(info_comm)


if __name__ == '__main__':
    main()
