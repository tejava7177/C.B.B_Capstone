import tensorflow as tf

# 모델 로드
model_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/training/lstm_chord_model2.h5"
model = tf.keras.models.load_model(model_path)

print("✅ 모델이 정상적으로 로드되었습니다!")