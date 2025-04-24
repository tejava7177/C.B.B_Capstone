# 📄 File: model/training/setLSTM_model5.py

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import os

# ✅ 경로 설정
base_dir = "/Users/simjuheun/Desktop/myProject/C.B.B/model/dataset/model/dataset"
X = np.load(os.path.join(base_dir, "X.npy"))
Y = np.load(os.path.join(base_dir, "Y.npy"))
chord_to_index = np.load(os.path.join(base_dir, "chord_to_index.npy"), allow_pickle=True).item()

NUM_CLASSES = len(chord_to_index)
SEQUENCE_LENGTH = 4
INPUT_SHAPE = (SEQUENCE_LENGTH, NUM_CLASSES)

# ✅ One-Hot 인코딩 (X는 정수 인덱스 배열이므로)
X = to_categorical(X, num_classes=NUM_CLASSES)

# ✅ 모델 정의
model = Sequential([
    LSTM(256, return_sequences=False, input_shape=INPUT_SHAPE),
    Dropout(0.3),
    Dense(128, activation="relu"),
    Dropout(0.2),
    Dense(NUM_CLASSES, activation="softmax")
])

model.compile(
    loss="categorical_crossentropy",
    optimizer=Adam(learning_rate=0.001),
    metrics=["accuracy"]
)

# ✅ 콜백 설정
early_stopping = EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
checkpoint_path = "model/training/lstm_chord_model5_best.h5"
model_checkpoint = ModelCheckpoint(
    checkpoint_path, monitor="val_loss", save_best_only=True, verbose=1
)

# ✅ 학습 시작
print("🚀 LSTM 모델 학습 시작...")
model.fit(
    X, Y,
    epochs=100,
    batch_size=256,
    validation_split=0.2,
    callbacks=[early_stopping, model_checkpoint]
)

# ✅ 최종 모델 저장
final_path = "model/training/lstm_chord_model5.h5"
model.save(final_path)
print(f"✅ 최종 모델 저장 완료: {final_path}")
