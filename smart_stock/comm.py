info_lv1 = {
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


import pandas as pd
import numpy as np
import random
import os

import tensorflow as tf
import comm

pd.set_option('display.max_columns', None)

def set_deterministic(info_lv1):
    seed = info_lv1['seed']
    np.random.seed(seed)
    random.seed(seed)

    if tf.__version__ == '1.14.0':
        from tfdeterminism import patch
        patch()
        os.environ['PYTHONHASHseed'] = '0'
        os.environ['TF_DETERMINISTIC_OPS'] = '1'
        os.environ['TF_CUDNN_DETERMINISTIC'] = '1'
        tf.set_seed(seed)
    elif tf.__version__ in ['2.5.0', '2.9.0']:
        os.environ['PYTHONHASHseed'] = '0'
        os.environ['TF_DETERMINISTIC_OPS'] = '1'
        os.environ['TF_CUDNN_DETERMINISTIC'] = '1'
        os.environ['TF_CUDNN_USE_FRONTEND '] = '1'  # https://github.com/tensorflow/tensorflow/issues/53771
        tf.random.set_seed(seed)  # https://github.com/keras-team/keras/blob/v2.10.0/keras/utils/tf_utils.py#L34-L66
    elif tf.__version__ == '2.10.0':
        tf.keras.utils.set_seed(seed)
        tf.config.experimental.enable_op_determinism()