import pandas as pd

info_comm = {
    'version': '0.1.0-alpha',

    'path_input': 'input_data',
    'path_output': 'output_data',
    'path_model': 'model',

    # get_company_code
    'df_krx': None,
    'dict_company_code': None,

    # select_target_company
    'num_of_target_company': 1,
    'target_company': None,
    'col_target': 'Stocks',     # 'ChagesRatio', 'Stocks'

    # get_data_naver_stock
    'page_cnt': 100,

    #
    'idx_train': None,
    'idx_test': None,
    'idx_blind': None,
    'list_col_y': None,
    'list_col_x': None,

    'scaler_x': None,
    'scaler_y': None,

    # make_model
    'model_name': 'dnn', # 'rf', 'dnn'
    'seed': 42,
    'params': {
        'n_estimators': (100, 200),
        'max_depth': (5, 8),
        'min_samples_leaf': (8, 18),
        'min_samples_split': (8, 16)
    },
}

pd.set_option('display.max_columns', None)