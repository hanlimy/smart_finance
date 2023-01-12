import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt


def get_nasdaq_quandl():
    path_output = 'output_data'

    import quandl
    quandl.ApiConfig.api_key = "h4m1wXxBGk62tH6XfeWa"

    df_gold = quandl.get("LBMA/GOLD", trim_start="2021-01-01", trim_end="2022-01-11")
    df_gold.to_csv('{}/df_gold.csv'.format(path_output))

    plt.rcParams["figure.figsize"] = (14, 4)
    plt.rcParams['axes.grid'] = True


get_nasdaq_quandl()