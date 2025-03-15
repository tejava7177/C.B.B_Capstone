# import tensorflow as tf
# from tensorflow.python.framework.errors_impl import NotFoundError
#
# # Apple Silicon Metal 지원 확인
# try:
#     from tensorflow.python.compiler.mlcompute import mlcompute
#     mlcompute.set_mlc_device(device_name='gpu')  # GPU 활성화 시도
#     print("✅ Apple Silicon GPU (Metal) 활성화 완료!")
# except ImportError:
#     print("❌ Apple Silicon GPU (Metal)을 사용할 수 없습니다. CPU로 학습을 진행합니다.")
# except NotFoundError as e:
#     print("❌ Metal 지원이 누락된 것 같습니다:", e)
#
# # 사용 가능한 장치 출력
# print("사용 가능한 장치 목록:", tf.config.list_physical_devices())


# import tensorflow as tf
#
# # GPU 활성화 가능 여부 확인
# gpus = tf.config.list_physical_devices('GPU')
# if gpus:
#     try:
#         tf.config.experimental.set_memory_growth(gpus[0], True)
#         print("✅ GPU 메모리 동적 할당 활성화 완료!")
#     except RuntimeError as e:
#         print("❌ GPU 설정 중 오류 발생:", e)
# else:
#     print("❌ 사용 가능한 GPU를 찾을 수 없습니다. CPU로 학습을 진행합니다.")
#
# # 사용 가능한 장치 확인
# print("사용 가능한 장치 목록:", tf.config.list_physical_devices())


import tensorflow as tf

# 실행 장치 출력
print("🔍 TensorFlow 실행 장치 확인:")
print(tf.config.list_logical_devices())

# GPU 연산 테스트 (기본 행렬 곱셈)
with tf.device('/GPU:0'):
    a = tf.random.normal([1000, 1000])
    b = tf.random.normal([1000, 1000])
    c = tf.matmul(a, b)

print("✅ GPU에서 연산이 수행되었습니다!")