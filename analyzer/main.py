from collector import get_data_from_src
from visual import make_page


def main():

    info_comm = {
        'date_start': '2022-01-01',
        'date_end': '2022-12-31',
        'path_output': 'output_data',

        'index_stock': [
            'KRX', 'NASDAQ', 'S&P500'
        ],

        'src_material': {
            'gold': 'LBMA/GOLD',
            'silver': 'LBMA/SILVER',
            'copper': 'CHRIS/CME_HG10',
            'oil': 'OPEC/ORB',
        },

        'src_kosdaq': {
            'sec': '005930',
        },

        'src_nasdaq': {
            'apple': 'AAPL'
        }


    }

    # get_data_from_src(info_comm)
    make_page(info_comm)


if __name__ == '__main__':
    main()
