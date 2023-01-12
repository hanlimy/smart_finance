import pandas as pd
import numpy as np
import math
import random
import re
import os
import joblib

from sklearn.ensemble import RandomForestRegressor

import tensorflow as tf
from keras import Input, Model, backend
from keras.layers import Reshape, Conv1D, Lambda, Flatten, Dense
from keras.utils import set_random_seed
from keras.callbacks import EarlyStopping
from comm import set_deterministic


def make_model(info_lv2, box_study_scaled):
    print('-' * 100 + '\n[make_model]')
    print(' > Tensorflow ver. : {}'.format(tf.__version__))

    set_deterministic(info_lv2)

    smart_stock = dict()
    for company in info_lv2['target_company']:
        print(' > company : {}'.format(company))
        
        df_study_scaled = box_study_scaled[company]

        list_col_x = info_lv2['list_col_x']
        list_col_y = info_lv2['list_col_y']
        idx_train = info_lv2['idx_train']
        idx_test = info_lv2['idx_test']
        idx_blind = info_lv2['idx_blind']

        x_train_s = df_study_scaled.loc[idx_train, list_col_x]
        x_test_s = df_study_scaled.loc[idx_test, list_col_x]
        y_train_s = df_study_scaled.loc[idx_train, list_col_y]
        y_test_s = df_study_scaled.loc[idx_test, list_col_y]

        if info_lv2['model_name'] == 'rf':
            print('  >> model_name : {}'.format(info_lv2['model_name']))
            model = RandomForestRegressor(random_state=info_lv2['seed'], n_jobs=-1)
            model.fit(x_train_s, y_train_s)
            # grid_cv = GridSearchCV(model, param_grid=info_lv2['params'], cv=2, n_jobs=-1)

        elif info_lv2['model_name'] == 'dnn':
            print('  >> model_name : ', info_lv2['model_name'])
            print('  >> tensorflow ver.: ', tf.__version__)
            print('  >> Num GPUs Available: ', len(tf.config.experimental.list_physical_devices('GPU')))
            print('  >> Num GPUs Available (list_physical_devices): ', tf.config.list_physical_devices('GPU'))

            x_shape = x_train_s.shape[1]
            print('  >> x_shape : ', x_shape)

            xInput = Input(shape=(x_shape, ))
            xReshape = Reshape((x_shape, 1))(xInput)
            xConv1D = Conv1D(int(x_shape / 2), 20, padding='same', activation='tanh')(xReshape)
            xPooling = Lambda(lambda x: backend.mean(x, axis=2)[:, None, :])(xConv1D)
            xFlatten = Flatten()(xPooling)
            xDense1 = Dense(int(x_shape), activation='relu',)(xFlatten)
            xDense2 = Dense(int(x_shape), activation='relu',)(xDense1)
            xOutput = Dense(int(1),)(xDense2)
            model = Model(xInput, xOutput)

            model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
            model.fit(
                x_train_s, y_train_s, epochs=100, batch_size=10, validation_data=(x_test_s, y_test_s),
                callbacks=EarlyStopping(
                    monitor='val_loss', patience=10, restore_best_weights=True
                )
            )
            model.save('{}/model_smart_stock_{}.h5'.format(info_lv2['path_model'], company))

        smart_stock[company] = dict()
        smart_stock[company]['model'] = model

    joblib.dump(smart_stock, '{}/model_smart_stock.pkl'.format(info_lv2['path_model']))
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
