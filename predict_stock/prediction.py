import pandas as pd

from sklearn.metrics import mean_squared_error, accuracy_score, precision_score, recall_score, r2_score


def simple_prediction(info_lv2, smart_stock, box_study_sampled, box_study_scaled):
    print('-' * 100 + '\n[simple_prediction]')

    for company in info_lv2['target_company']:
        print(' > company : {}'.format(company))
        df_study_sampled = box_study_sampled[company]
        df_study_scaled = box_study_scaled[company]

        list_col_x = info_lv2['list_col_x']
        list_col_y = info_lv2['list_col_y']
        idx_train = info_lv2['idx_train']
        idx_test = info_lv2['idx_test']
        idx_blind = info_lv2['idx_blind']

        x_train = df_study_sampled.loc[idx_train, list_col_x]
        x_test = df_study_sampled.loc[idx_test, list_col_x]
        y_train = df_study_sampled.loc[idx_train, list_col_y]
        y_test = df_study_sampled.loc[idx_test, list_col_y]

        x_train_s = df_study_scaled.loc[idx_train, list_col_x]
        x_test_s = df_study_scaled.loc[idx_test, list_col_x]

        x_minmax = pd.DataFrame(columns=x_train.columns)
        print(' > x_train_test_minmax')
        x_minmax = pd.concat([
            x_minmax,
            pd.DataFrame(x_train.max()).T.rename({0: 'x_train_max'}),
            pd.DataFrame(x_train.min()).T.rename({0: 'x_train_min'}),
            pd.DataFrame(x_test.max()).T.rename({0: 'x_test_max'}),
            pd.DataFrame(x_test.min()).T.rename({0: 'x_test_min'}),
            pd.DataFrame(x_train_s.max()).T.rename({0: 'x_train_s_max'}),
            pd.DataFrame(x_train_s.min()).T.rename({0: 'x_train_s_min'}),
            pd.DataFrame(x_test_s.max()).T.rename({0: 'x_test_s_max'}),
            pd.DataFrame(x_test_s.min()).T.rename({0: 'x_test_s_min'}),
        ])
        print(x_minmax)

        model = smart_stock[company]['model']
        y_test_pred_s = model.predict(x_test_s)
        y_test_pred = pd.DataFrame(info_lv2['scaler_y'].inverse_transform(y_test_pred_s), columns=y_train.columns)

        df_study_sampled['y_test'] = df_study_sampled[company + '_price_end']

        idx_test = info_lv2['idx_test']
        df_study_sampled.loc[idx_test, 'y_test_pred'] = y_test_pred.values

        df_study_sampled.to_csv('{}/4-01-01_df_study_sampled_pred.csv'.format(info_lv2['path_output']))

        print('  >> R2 : {}'.format(r2_score(y_test, y_test_pred)))