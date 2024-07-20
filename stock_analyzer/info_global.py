


def get_info_comm():

    path_output = 'output_data'
    date_start = '2023-01-01'
    date_today = '2023-12-31'

    info_comm = {
        'path_output': path_output,

        'date_start': date_start,
        'date_end': date_today,

        'item_code': {
            'KRX': None,
            # 'NASDAQ': None,
            # 'S&P500': None,
        },
    }

    return info_comm