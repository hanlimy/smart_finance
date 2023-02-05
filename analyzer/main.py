from collector import update_info_comm, get_data_from_src
from visual import make_page


def main():

    info_comm = {
        'date_start': '2022-01-01',
        'date_end': '2023-02-05',
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

    info_comm = update_info_comm(info_comm)
    # get_data_from_src(info_comm)
    make_page(info_comm)


if __name__ == '__main__':
    main()
