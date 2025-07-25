import pandas as pd
import requests as rq
import FinanceDataReader as fdr
from bs4 import BeautifulSoup

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
from keras import Input, Model, backend
from keras.layers import Reshape, Conv1D, Lambda, Flatten, Dense
from keras.callbacks import EarlyStopping

import numpy as np
import random
import os


def get_company_code(info_comm):
    print('-' * 100 + '\n[get_company_code]')

    df_krx = fdr.StockListing('KRX')
    df_krx.to_csv('{}/1-01-01_df_krx.csv'.format(info_comm['path_output']))
    info_comm['df_krx'] = df_krx

    df_krx_code = df_krx[['Code', 'Name']].set_index('Name')
    dict_krk_code = df_krx_code.to_dict()['Code']
    info_comm['dict_company_code'] = dict_krk_code
    print(' > dict_krk_code : {}'.format(dict_krk_code))


def select_target_company(info_comm):
    print('-' * 100 + '\n[select_target_company]')

    df_krx = info_comm['df_krx']
    num_com = info_comm['num_of_target_company']

    col_target = info_comm['col_target']

    # info_comm['target_company'] = ['삼성전자', '삼성SDI']
    info_comm['target_company'] = list(df_krx.sort_values(col_target, ascending=False)['Name'].iloc[0:num_com])
    print(' > target_company : {}'.format(info_comm['target_company']))


def get_data_naver_stock(info_comm):
    print('-' * 100 + '\n[get_data_naver_stock]')

    company_code = info_comm['dict_company_code']
    df_price_all = pd.DataFrame()

    for company_name in info_comm['target_company']:
        code = company_code[company_name]
        print(' > name : {} | code : {}'.format(company_name, code))

        url = f'https://finance.naver.com/item/sise_day.naver?code={code}'
        headers = {'User-agent': 'Mozilla/5.0'}
        req = rq.get(url, headers=headers)
        html = BeautifulSoup(req.text, 'lxml')

        pgrr = html.find('td', class_='pgRR')
        s = pgrr.a['href'].split('=')
        last_page = int(s[-1])

        page_start = 1
        page_last = page_start + info_comm['page_cnt']

        df_price = pd.DataFrame()
        for page in range(page_start, page_last):
            print('  >> web page : {} / {}'.format(page, last_page))
            req = rq.get(f'{url}&page={page}', headers=headers)
            df_price = pd.concat([df_price, pd.read_html(req.text, encoding='euc-kr')[0]], ignore_index=True)

        df_price = df_price.dropna().reset_index(drop=True)
        df_price = df_price.rename(columns={
            '날짜': 'date',
            '거래량': 'vol_exch',
            '종가': 'price_end',
            '고가': 'price_high',
            '저가': 'price_low',
        })
        df_price = df_price[['date', 'vol_exch', 'price_end', 'price_high', 'price_low']]
        # df_price_end = df_price[['date', 'vol_exch', 'price_end']]
        # df_price_end = df_price_end.rename(columns={'price_end': 'price_' + name, 'vol_exch': 'vol_' + name})

        df_price.columns = [company_name + '_' + col if col not in ['date'] else col for col in df_price.columns]

        if len(df_price_all):
            df_price_all = pd.merge(df_price_all, df_price, on='date', how='right')
        else:
            df_price_all = df_price

    df_price_all = df_price_all.sort_values('date', ascending=True).reset_index(drop=True)
    df_price_all.to_csv('{}/1-01-99_price_company.csv'.format(info_comm['path_output']))

    # list_date = list(df_price_all['date'].apply(lambda x: x.split('.')[1] + '/' + x.split('.')[2]))
    #
    # for name in info_comm['target_company']:
    #     plt.plot(
    #         list_date,
    #         df_price_all['price_' + name]
    #         # label=name
    #     )
    #
    # plt.xticks([list_date[0], list_date[int(len(list_date)/2)], list_date[-1]], rotation=45)
    #
    # plt.legend(loc=(0.05, 0.05))
    # file_name = '{}/price_history.png'.format(info_comm['path_output'])
    # plt.show(block=False)
    # plt.savefig(file_name)
    # plt.pause(1)
    # plt.close()


def sampling(info_comm):
    print('-' * 100 + '\n[sampling]')

    set_deterministic(info_comm)

    df_study = pd.read_csv('{}/1-01-99_price_company.csv'.format(info_comm['path_output']), index_col=0)

    if info_comm['target_company'] is None:
        col_sample = [df_study.columns[0].split('_')[0]]
        print(' > info_comm_target_company is Null, select first col in df_study : {}'.format(col_sample))
        info_comm['target_company'] = col_sample

    box_study = dict()
    for company in info_comm['target_company']:
        print(' > company : {}'.format(company))
        list_col_study = [col for col in df_study if company in col]

        # catch_y = re.compile('price[0-9a-zA-Z._-]*')
        # print(catch_y.match(''))

        df_study['usage'] = 'train'
        idx_blind = sorted(df_study[df_study['date'] > '2023-01-01'].index)
        df_study.loc[idx_blind, 'usage'] = 'blind'

        idx_tt = sorted(df_study[df_study['usage'] != 'blind'].index)
        idx_test = sorted(random.sample(idx_tt, 10))
        idx_train = [idx for idx in idx_tt if idx not in idx_test]
        df_study.loc[idx_test, 'usage'] = 'test'
        df_study.loc[idx_train, 'usage'] = 'train'
        df_study.to_csv('{}/2-01-01_df_study_sampled.csv'.format(info_comm['path_output']))

        print('  >> idx_train : {}'.format(idx_train))
        print('  >> idx_test : {}'.format(idx_test))
        print('  >> idx_blind : {}'.format(idx_blind))
        info_comm['idx_train'] = idx_train
        info_comm['idx_test'] = idx_test
        info_comm['idx_blind'] = idx_blind

        col_y = 'price_end'
        list_col_x = [col for col in list_col_study if col_y not in col]
        # list_col_x = list_col_x[0:1]
        list_col_y = [col for col in list_col_study if col_y in col]
        print('  >> list_col_study : {}'.format(list_col_study))
        print('  >> list_col_x : {}'.format(list_col_x))
        print('  >> list_col_y : {}'.format(list_col_y))
        info_comm['list_col_x'] = list_col_x
        info_comm['list_col_y'] = list_col_y

        box_study[company] = df_study

    return box_study


def scaling(info_comm, box_study_sampled):
    print('-' * 100 + '\n[scaling]')

    box_study_scaled = dict()

    for company in info_comm['target_company']:
        print(' > company : {}'.format(company))
        df_study = box_study_sampled[company]
        list_col_x = info_comm['list_col_x']
        list_col_y = info_comm['list_col_y']
        idx_train = info_comm['idx_train']
        idx_test = info_comm['idx_test']
        idx_blind = info_comm['idx_blind']

        df_study_scaled = df_study.copy()

        scaler_x = MinMaxScaler()
        scaler_x.fit(df_study.loc[idx_train, list_col_x])
        x_train_s = scaler_x.transform(df_study.loc[idx_train, list_col_x])
        x_test_s = scaler_x.transform(df_study.loc[idx_test, list_col_x])
        x_blind_s = scaler_x.transform(df_study.loc[idx_blind, list_col_x])

        scaler_y = MinMaxScaler()
        scaler_y.fit(df_study.loc[idx_train, list_col_y])
        y_train_s = scaler_y.transform(df_study.loc[idx_train, list_col_y])
        y_test_s = scaler_y.transform(df_study.loc[idx_test, list_col_y])
        y_blind_s = scaler_y.transform(df_study.loc[idx_blind, list_col_y])

        df_study_scaled.loc[idx_train, list_col_x] = x_train_s
        df_study_scaled.loc[idx_test, list_col_x] = x_test_s
        df_study_scaled.loc[idx_blind, list_col_x] = x_blind_s
        df_study_scaled.loc[idx_train, list_col_y] = y_train_s
        df_study_scaled.loc[idx_test, list_col_y] = y_test_s
        df_study_scaled.loc[idx_blind, list_col_y] = y_blind_s
        df_study_scaled.to_csv('{}/2-02-01_df_study_scaled.csv'.format(info_comm['path_output']))

        info_comm['scaler_x'] = scaler_x
        info_comm['scaler_y'] = scaler_y

        print('  >> x_train_s.shape : {}'.format(x_train_s.shape))
        print('  >> x_test_s.shape : {}'.format(x_test_s.shape))

        box_study_scaled[company] = df_study_scaled

    return box_study_scaled


def set_deterministic(info_comm):
    seed = info_comm['seed']
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


def make_model(info_comm, box_study_scaled):
    print('-' * 100 + '\n[make_model]')
    print(' > Tensorflow ver. : {}'.format(tf.__version__))

    set_deterministic(info_comm)

    smart_stock = dict()
    for company in info_comm['target_company']:
        print(' > company : {}'.format(company))

        df_study_scaled = box_study_scaled[company]

        list_col_x = info_comm['list_col_x']
        list_col_y = info_comm['list_col_y']
        idx_train = info_comm['idx_train']
        idx_test = info_comm['idx_test']
        idx_blind = info_comm['idx_blind']

        x_train_s = df_study_scaled.loc[idx_train, list_col_x]
        x_test_s = df_study_scaled.loc[idx_test, list_col_x]
        y_train_s = df_study_scaled.loc[idx_train, list_col_y]
        y_test_s = df_study_scaled.loc[idx_test, list_col_y]

        if info_comm['model_name'] == 'rf':
            print('  >> model_name : {}'.format(info_comm['model_name']))
            model = RandomForestRegressor(random_state=info_comm['seed'], n_jobs=-1)
            model.fit(x_train_s, y_train_s)
            # grid_cv = GridSearchCV(model, param_grid=info_comm['params'], cv=2, n_jobs=-1)

        elif info_comm['model_name'] == 'dnn':
            print('  >> model_name : ', info_comm['model_name'])
            print('  >> tensorflow ver.: ', tf.__version__)
            print('  >> Num GPUs Available: ', len(tf.config.experimental.list_physical_devices('GPU')))
            print('  >> Num GPUs Available (list_physical_devices): ', tf.config.list_physical_devices('GPU'))

            x_shape = x_train_s.shape[1]
            print('  >> x_shape : ', x_shape)

            xInput = Input(shape=(x_shape,))
            xReshape = Reshape((x_shape, 1))(xInput)
            xConv1D = Conv1D(int(x_shape / 2), 20, padding='same', activation='tanh')(xReshape)
            xPooling = Lambda(lambda x: backend.mean(x, axis=2)[:, None, :])(xConv1D)
            xFlatten = Flatten()(xPooling)
            xDense1 = Dense(int(x_shape), activation='relu', )(xFlatten)
            xDense2 = Dense(int(x_shape), activation='relu', )(xDense1)
            xOutput = Dense(int(1), )(xDense2)
            model = Model(xInput, xOutput)

            model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
            model.fit(
                x_train_s, y_train_s, epochs=100, batch_size=10, validation_data=(x_test_s, y_test_s),
                callbacks=EarlyStopping(
                    monitor='val_loss', patience=10, restore_best_weights=True
                )
            )
            model.save('{}/model_smart_stock_{}.h5'.format(info_comm['path_model'], company))

        smart_stock[company] = dict()
        smart_stock[company]['model'] = model

    joblib.dump(smart_stock, '{}/model_smart_stock.pkl'.format(info_comm['path_model']))
    # joblib.load('smart_stock.pkl')

    return smart_stock


def make_model_example():
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=5)
    model.evaluate(x_test, y_test, verbose=2)