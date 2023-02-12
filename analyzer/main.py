from collector import make_index_file_from_db, make_box_code_from_index_file, get_data_from_db
from visual import make_page
from datetime import datetime


def main():

    today = datetime.now().strftime('%Y-%m-%d')

    info_comm = {

        'date_start': '2022-01-01',
        'date_end': today,
        'path_output': 'output_data',

        'box_code': {
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

    # make_index_file_from_db(info_comm)
    # info_comm = make_box_code_from_index_file(info_comm)
    # get_data_from_db(info_comm)
    make_page(info_comm)


if __name__ == '__main__':
    main()
