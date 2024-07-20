from info_global import *
from engine import *
from prediction import *


if __name__ == '__main__':
    print('#' * 100 + '\n[smart_stock] {}'.format(info_comm['version']))

    # 1. get data
    print('#' * 100 + '\n[get_data]')
    get_company_code(info_comm)
    select_target_company(info_comm)
    get_data_naver_stock(info_comm)

    # 2. Pre Processing
    print('#' * 100 + '\n[pre_proc]')
    box_study_sampled = sampling(info_comm)
    box_study_scaled = scaling(info_comm, box_study_sampled)

    # 3. Modeling
    print('#' * 100 + '\n[simple_modeling]')
    smart_stock = make_model(info_comm, box_study_scaled)

    # 4. Predict
    print('#' * 100 + '\n[prediction]')
    simple_prediction(info_comm, smart_stock, box_study_sampled, box_study_scaled)