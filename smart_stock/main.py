from comm import info_lv1
from getdata import get_company_code, select_target_company, get_data_naver_stock
from preproc import sampling, scaling
from engine import make_model
from prediction import simple_prediction


if __name__ == '__main__':
    print('#' * 100 + '\n[smart_stock] {}'.format(info_lv1['version']))

    # 1. get data
    print('#' * 100 + '\n[get_data]')
    get_company_code(info_lv1)
    select_target_company(info_lv1)
    get_data_naver_stock(info_lv1)

    # 2. Pre Processing
    print('#' * 100 + '\n[pre_proc]')
    box_study_sampled = sampling(info_lv1)
    box_study_scaled = scaling(info_lv1, box_study_sampled)

    # 3. Modeling
    print('#' * 100 + '\n[simple_modeling]')
    smart_stock = make_model(info_lv1, box_study_scaled)

    # 4. Predict
    print('#' * 100 + '\n[prediction]')
    simple_prediction(info_lv1, smart_stock, box_study_sampled, box_study_scaled)
