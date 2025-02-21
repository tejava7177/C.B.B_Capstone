import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.utils import to_categorical

# 데이터 로드
X = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/X.npy")
Y = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/Y.npy")

# 하이퍼파라미터 설정
SEQUENCE_LENGTH = X.shape[1]  # 자동 설정 (현재 3)
NUM_CLASSES = Y.shape[1]  # 고유 코드 개수 (현재 42개)

# 모델 하이퍼파라미터
EMBEDDING_DIM = 32
LSTM_UNITS = 128
BATCH_SIZE = 128
EPOCHS = 50

# LSTM 모델 생성
model = Sequential([
    Embedding(input_dim=NUM_CLASSES, output_dim=EMBEDDING_DIM, input_length=SEQUENCE_LENGTH),
    LSTM(LSTM_UNITS, return_sequences=True),
    LSTM(LSTM_UNITS),
    Dense(64, activation='relu'),
    Dense(NUM_CLASSES, activation='softmax')
])

# 모델 컴파일
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 모델 학습
history = model.fit(X, Y, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.1)

# 학습된 모델 저장
model.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/training/lstm_chord_model3.h5")

print("✅ 새로운 LSTM 모델 학습 완료 및 저장 완료!")