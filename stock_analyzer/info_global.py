from datetime import datetime


def get_now(type_now):
    if type_now == 'DATE':
        now = datetime.now().strftime('%Y-%m-%d')
    elif type_now == 'TIME':
        now = datetime.now().strftime('%y%m%d-%H:%M:%S')
    else:
        now = None

    return now


def get_info_comm():

    path_output = 'output_data'

    date_start = '2024-01-01'
    date_today = get_now('DATE')

    # list_item_src = ['KRX', 'NASDAQ', 'S&P500']
    list_item_src = ['KRX']

    info_comm = {
        'path_output': path_output,

        'date_start': date_start,
        'date_end': date_today,

        'list_item_src': list_item_src,
        'dict_item_code': None,
    }

    return info_comm

