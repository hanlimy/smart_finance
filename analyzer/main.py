from collector import get_nasdaq_quandl
from visual import make_page


def main():

    info_comm = {
        'date_start': '2022-01-01',
        'date_end': '2022-12-31',
        'path_output': 'output_data',

        'src_nasdaq': {
            'gold': 'LBMA/GOLD',
            'silver': 'LBMA/SILVER',
            'copper': 'CHRIS/CME_HG10',
            'oil': 'OPEC/ORB',
        },
    }

    # get_nasdaq_quandl(info_comm)
    make_page(info_comm)


if __name__ == '__main__':
    main()
