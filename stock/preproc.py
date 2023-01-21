import pandas as pd
import random

from sklearn.preprocessing import MinMaxScaler
from comm import set_deterministic


def sampling(info_lv2):
    print('-' * 100 + '\n[sampling]')

    set_deterministic(info_lv2)

    df_study = pd.read_csv('{}/1-01-99_price_company.csv'.format(info_lv2['path_output']), index_col=0)

    if info_lv2['target_company'] is None:
        col_sample = [df_study.columns[0].split('_')[0]]
        print(' > info_lv2_target_company is Null, select first col in df_study : {}'.format(col_sample))
        info_lv2['target_company'] = col_sample

    box_study = dict()
    for company in info_lv2['target_company']:
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
        df_study.to_csv('{}/2-01-01_df_study_sampled.csv'.format(info_lv2['path_output']))

        print('  >> idx_train : {}'.format(idx_train))
        print('  >> idx_test : {}'.format(idx_test))
        print('  >> idx_blind : {}'.format(idx_blind))
        info_lv2['idx_train'] = idx_train
        info_lv2['idx_test'] = idx_test
        info_lv2['idx_blind'] = idx_blind

        col_y = 'price_end'
        list_col_x = [col for col in list_col_study if col_y not in col]
        # list_col_x = list_col_x[0:1]
        list_col_y = [col for col in list_col_study if col_y in col]
        print('  >> list_col_study : {}'.format(list_col_study))
        print('  >> list_col_x : {}'.format(list_col_x))
        print('  >> list_col_y : {}'.format(list_col_y))
        info_lv2['list_col_x'] = list_col_x
        info_lv2['list_col_y'] = list_col_y

        box_study[company] = df_study
        
    return box_study


def scaling(info_lv2, box_study_sampled):
    print('-' * 100 + '\n[scaling]')

    box_study_scaled = dict()

    for company in info_lv2['target_company']:
        print(' > company : {}'.format(company))
        df_study = box_study_sampled[company]
        list_col_x = info_lv2['list_col_x']
        list_col_y = info_lv2['list_col_y']
        idx_train = info_lv2['idx_train']
        idx_test = info_lv2['idx_test']
        idx_blind = info_lv2['idx_blind']

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
        df_study_scaled.to_csv('{}/2-02-01_df_study_scaled.csv'.format(info_lv2['path_output']))

        info_lv2['scaler_x'] = scaler_x
        info_lv2['scaler_y'] = scaler_y

        print('  >> x_train_s.shape : {}'.format(x_train_s.shape))
        print('  >> x_test_s.shape : {}'.format(x_test_s.shape))

        box_study_scaled[company] = df_study_scaled

    return box_study_scaled
