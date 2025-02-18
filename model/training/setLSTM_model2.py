import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.utils import to_categorical

# 데이터 로드
X = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/X.npy")
Y = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/Y.npy")
NUM_CLASSES = Y.shape[1]  # 🔥 43개 코드 반영

# 모델 하이퍼파라미터
EMBEDDING_DIM = 16
LSTM_UNITS = 64
BATCH_SIZE = 64
EPOCHS = 50

# LSTM 모델 생성
model = Sequential([
    Embedding(input_dim=NUM_CLASSES, output_dim=EMBEDDING_DIM, input_length=X.shape[1]),
    LSTM(LSTM_UNITS, return_sequences=True),
    LSTM(LSTM_UNITS),
    Dense(64, activation='relu'),
    Dense(NUM_CLASSES, activation='softmax')
])

# 모델 컴파일
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 모델 학습
history = model.fit(X, Y, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.1)

# 모델 저장
model.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/training/lstm_chord_model2.h5")

print("✅ 새롭게 학습된 LSTM 모델 저장 완료!")