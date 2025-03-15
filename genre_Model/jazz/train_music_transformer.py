import numpy as np
import tensorflow as tf
import os
from music_transformer_model import MusicTransformer  # ✅ 모델을 새 파일에서 불러오기!

# ✅ 데이터 로드
dataset_dir = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/"
X = np.load(os.path.join(dataset_dir, "X.npy"))
y = np.load(os.path.join(dataset_dir, "y.npy"))

# ✅ 하이퍼파라미터 설정
sequence_length = 10
d_model = 256
num_heads = 16
dff = 1024
num_layers = 6
vocab_size = 128
batch_size = 128
epochs = 100

# ✅ 모델 생성
model = MusicTransformer(sequence_length, d_model, num_heads, dff, num_layers, vocab_size)

# ✅ 모델 컴파일
model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    metrics=['accuracy']
)

# ✅ Early Stopping 콜백 추가
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',  # 검증 손실이 개선되지 않으면 조기 종료
    patience=20,  # 20 epoch 동안 개선되지 않으면 멈춤
    restore_best_weights=True  # 가장 성능이 좋았던 모델의 가중치 복원
)


# ✅ 모델 학습
history = model.fit(X, y, batch_size=batch_size, epochs=epochs, validation_split=0.2, callbacks=[early_stopping])

# ✅ 학습 로그 저장
history_path = os.path.join(dataset_dir, "history.npy")
np.save(history_path, history.history)
print(f"📂 학습 로그 저장 완료: {history_path}")

# ✅ 모델 저장 (Keras 형식)
model.save(os.path.join(dataset_dir, "music_transformer_jazz.keras"))
print("🎶 모델 저장 완료!")