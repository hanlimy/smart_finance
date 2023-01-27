# import tensorflow as tf

# gpu running is ok spec
# python 3.8.15
# tensorflow-deps 2.10.0
# tensorflow-macos 2.9.0
# tensorflowmetal 0.5.0

# test in ipad 1/17


def test_gpu_multi():
    print('tensorflow ver.: ', tf.__version__)
    print('Num GPUs Available: ', len(tf.config.experimental.list_physical_devices('GPU')))
    print('Num GPUs Available (list_physical_devices): ', tf.config.list_physical_devices('GPU'))

    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train/255.0, x_test/255.0

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=5)
    model.evaluate(x_test,  y_test, verbose=2)


def test_code():
    """ 원주율(파이) 계산하기 * 아르키메데스의 수 """
    import math  # math 모듈 불러 오기

    old_pi = 3.14163  # 아르키메데스가 96각형을 사용(n = 96)하여 계산한 원주율값
    n = 5  # 5각형부터 시작
    err = 0.000000001  # 허용오차 십억분의 일

    while True:
        degree = 360 / n  # n각형의 내각
        theta = degree / 2  # 내각의 절반이 삼각함수의 기준 각도(A)
        inner_length = math.sin(math.radians(theta)) * 2  # 내접하는 변의 길이 sin A * 2
        outer_length = math.tan(math.radians(theta)) * 2  # 외접하는 변의 길이 tan A * 2
        difference = outer_length - inner_length  # 내접하는 변과 외접하는 변의 길이 차이
        new_pi = n * ((outer_length + inner_length) / 2) / 2  # 중간값으로 원주율 계산

        # n값 증가에 따른 원주율 값, 오차 변화
        print("n: ", n, "new_pi: ", new_pi)
        if (difference < err):
            break  # 반복문 탈출
        else:
            n = n + 1  # 다각형의 변의 개수를 늘리기

    # 아르키메데스의 원주율과 계산값 차이 비교
    print("old_pi: ", old_pi, "new_pi: ", new_pi, "error: ", new_pi - old_pi)

    # 파이썬 내장 원주율값(math.pi)와 비교
    print("내장 원주율: ", math.pi, "차이: ", math.pi - new_pi)

