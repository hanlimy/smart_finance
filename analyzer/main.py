from collector import make_list_item_from_src, make_code_stock_item, get_price_stock
from visual import make_page
from datetime import datetime


def main():

    today = datetime.now().strftime('%Y-%m-%d')

    info_comm = {

        'date_start': '2022-01-01',
        'date_end': today,
        'path_output': 'output_data',

        'code_item_stock': {
            'KRX': None,

            'NASDAQ': None,
            'S&P500': None,

            # 'Material': {
            #     'gold': 'LBMA/GOLD',
            #     'silver': 'LBMA/SILVER',
            #     'copper': 'CHRIS/CME_HG10',
            #     'oil': 'OPEC/ORB',
            # },
        },
    }

    make_list_item_from_src(info_comm)
    info_comm = make_code_stock_item(info_comm)
    get_price_stock(info_comm)
    make_page(info_comm)


if __name__ == '__main__':
    main()
