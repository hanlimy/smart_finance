import pandas as pd
import numpy as np
import random

seed = 42
np.random.seed(seed)
random.seed(seed)


def make_df_study():
    path_output = 'output_data'

    list_col = ['CR0' + str(10 * step) for step in range(10000, 20000, 100)]

    print(' > len list_col : {} / first : {} / last : {}'.format(len(list_col), list_col[0], list_col[1]))
    df_study = pd.DataFrame(columns=list_col)

    random_max_split = 10
    box_ppid = ['PPID' + str(num) for num in range(10, 100)]

    for lot in ['BNN' + str(lot) for lot in range(100, 110)]:
        for wf in ['0' + str(wf) if wf < 10 else str(wf) for wf in range(1, 25)]:
            df_study.loc[lot + '_' + wf] = 0

    df_study = df_study.reset_index().rename(columns={'index': 'lot_wf'})

    for step in df_study.columns:
        if step == 'lot_wf':
            continue
        step_in_split = random.randint(4, random_max_split+1)
        list_idx_sample = sorted(random.sample(list(df_study.index), step_in_split-1))
        list_set_ppid = random.sample(box_ppid, step_in_split)
        print(' > step : {} | split : {} | list_idx_sample : {} | list_set_ppid : {}'.format(
            step, step_in_split, list_idx_sample, list_set_ppid))

        # make split point
        idx_start = 0
        for idx in range(0, len(list_idx_sample)):
            idx_end = list_idx_sample[idx]
            ppid = list_set_ppid[idx]
            df_study.loc[idx_start:idx_end, step] = ppid
            idx_start = idx_end

    df_study = df_study.set_index('lot_wf', drop=True)

    # make et
    # make chip_x_pos, chip_y_pos
    et_mean = 0.600
    for idx in df_study.index:
        df_study.at[idx, 'et'] = et_mean + random.random()

    list_pos_xy = [
        [3, 3], [5, 6], [2, -4], [4, -1],
        [-2, 5], [-4, 6], [-1, -3], [-6, -5],
    ]
    for idx in df_study.index:
        chip_pos = random.sample(list_pos_xy, 1)[0]
        df_study.at[idx, 'chip_x_pos'] = str(int(chip_pos[0]))
        df_study.at[idx, 'chip_y_pos'] = str(int(chip_pos[1]))

    df_study.to_csv('{}/df_study.csv'.format(path_output))


make_df_study()

