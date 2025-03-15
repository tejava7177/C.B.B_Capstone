import tensorflow as tf
import time


gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)  # 메모리 동적 할당
        print("✅ GPU 메모리 동적 할당 활성화 완료!")
    except RuntimeError as e:
        print(f"❌ GPU 메모리 설정 중 오류 발생: {e}")

# 모델 정의 (간단한 LSTM)
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(64, input_shape=(10, 1)),
    tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(loss='categorical_crossentropy', optimizer='adam')

# 더미 데이터 생성
X = tf.random.normal([1000, 10, 1])
y = tf.keras.utils.to_categorical(tf.random.uniform([1000], maxval=10, dtype=tf.int32), num_classes=10)

# CPU 실행
with tf.device('/CPU:0'):
    start = time.time()
    model.fit(X, y, epochs=1, batch_size=32, verbose=0)
    cpu_time = time.time() - start
    print(f"⚡ CPU 학습 시간: {cpu_time:.2f}초")

# GPU 실행
with tf.device('/GPU:0'):
    start = time.time()
    model.fit(X, y, epochs=1, batch_size=32, verbose=0)
    gpu_time = time.time() - start
    print(f"🚀 GPU 학습 시간: {gpu_time:.2f}초")

# 결과 비교
if gpu_time < cpu_time:
    print("✅ GPU가 정상적으로 작동 중입니다!")
else:
    print("❌ GPU가 활성화되었지만, 학습이 CPU보다 느릴 수 있습니다.")