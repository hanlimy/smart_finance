import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

seed = 42
np.random.seed(seed)
random.seed(seed)


def get_nasdaq_quandl():
    path_output = 'output_data'

    import quandl
    quandl.ApiConfig.api_key = "h4m1wXxBGk62tH6XfeWa"

    date_start = '2021-01-01'
    date_end = '2022-01-13'

    df_gold = quandl.get("LBMA/GOLD", trim_start=date_start, trim_end=date_end)
    df_silver = quandl.get("LBMA/SILVER", trim_start=date_start, trim_end=date_end)
    df_copper = quandl.get("CHRIS/CME_HG10", trim_start=date_start, trim_end=date_end)
    df_oil = quandl.get("OPEC/ORB", trim_start=date_start, trim_end=date_end)

    df_gold.to_csv('{}/df_gold.csv'.format(path_output))
    df_silver.to_csv('{}/df_silver.csv'.format(path_output))
    df_copper.to_csv('{}/df_copper.csv'.format(path_output))
    df_oil.to_csv('{}/df_oil.csv'.format(path_output))


def get_kosdaq_fdr():
    import FinanceDataReader as fdr

    df_krx = fdr.StockListing('KRX')
    df_appl = fdr.DataReader('AAPL', '2020-01-01', '2020-01-30')


def get_kor_pdr():
    from PublicDataReader import Kbland

    api = Kbland()
    params = {
        "월간주간구분코드": "01",
        "매물종별구분": "01",
        "매매전세코드": "01",
        # "지역코드": "11",
        "기간": 1,
    }
    df = api.get_price_index(**params)
    print(df.tail())


def make_df_study():
    path_output = 'output_data'

    list_col = ['CR0' + str(10 * step) for step in range(10000, 20000, 100)]

    print(' > len list_col : {} / first : {} / last : {}'.format(len(list_col), list_col[0], list_col[1]))
    df_study = pd.DataFrame(columns=list_col)

    random_max_split = 5
    box_ppid = ['PPID' + str(num) for num in range(10, 100)]

    for lot in ['BNN' + str(lot) for lot in range(100, 110)]:
        for wf in ['0' + str(wf) if wf < 10 else str(wf) for wf in range(1, 25)]:
            df_study.loc[lot + '_' + wf] = 0

    df_study = df_study.reset_index().rename(columns={'index': 'lot_wf'})

    for step in df_study.columns:
        if step == 'lot_wf':
            continue
        step_in_split = random.randint(2, random_max_split+1)
        list_idx_sample = sorted(random.sample(list(df_study.index), step_in_split-1))
        list_set_ppid = random.sample(box_ppid, step_in_split)
        print(' > step : {} | split : {} | list_idx_sample : {} | list_set_ppid : {}'.format(
            step, step_in_split, list_idx_sample, list_set_ppid))

        idx_start = 0
        for idx in range(0, len(list_idx_sample)):
            idx_end = list_idx_sample[idx]
            ppid = list_set_ppid[idx]
            df_study.loc[idx_start:idx_end, step] = ppid
            idx_start = idx_end

    df_study = df_study.set_index('lot_wf', drop=True)
    df_study.to_csv('{}/df_study.csv'.format(path_output))

make_df_study()

