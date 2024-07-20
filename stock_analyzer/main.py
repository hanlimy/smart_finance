from info_global import get_info_comm
from engine import *
from visualizer import *


def main_analyer():
    time_before = get_now('TIME')
    print('-' * 100)
    print('[main_analyer]-START() <{}>'.format(get_now('TIME')))

    info_comm = get_info_comm()

    # make_list_item_from_src(info_comm)
    make_stock_item_code(info_comm)

    # get_naver_finance_basic(info_comm)
    # get_price_stock(info_comm)

    filter_price_stock(info_comm)

    print('-' * 100)
    print('[main_analyzer]-END() <{} | {}>'.format(time_before, get_now('TIME')))


if __name__ == '__main__':
    main_analyer()
