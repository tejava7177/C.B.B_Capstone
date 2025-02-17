import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.utils import to_categorical

# 데이터 로드
chord_sequences = np.load("chord_sequences.npy")
chord_to_index = np.load("chord_to_index.npy", allow_pickle=True).item()
index_to_chord = {v: k for k, v in chord_to_index.items()}  # 역매핑

# 하이퍼파라미터 설정
SEQUENCE_LENGTH = 3  # LSTM이 이전 몇 개의 코드를 보고 다음 코드 예측할지 결정
NUM_CLASSES = len(chord_to_index)  # ⚠️ 전체 코드 개수 추가 (오류 해결)

# 입력(X)과 출력(Y) 생성
X, Y = [], []

for seq in chord_sequences:
    for i in range(len(seq) - SEQUENCE_LENGTH):
        X.append(seq[i:i + SEQUENCE_LENGTH])
        Y.append(seq[i + SEQUENCE_LENGTH])

X = np.array(X)
Y = np.array(Y)

# 출력(Y)을 One-Hot Encoding 변환
Y = to_categorical(Y, num_classes=NUM_CLASSES)

print(f"✅ 데이터셋 준비 완료! (X: {X.shape}, Y: {Y.shape})")
print(f"🎵 고유 코드 개수: {NUM_CLASSES}")

# 모델 하이퍼파라미터
EMBEDDING_DIM = 16  # 코드 벡터화 차원
LSTM_UNITS = 64  # LSTM 뉴런 개수
BATCH_SIZE = 64
EPOCHS = 50

# LSTM 모델 생성
model = Sequential([
    Embedding(input_dim=NUM_CLASSES, output_dim=EMBEDDING_DIM, input_length=SEQUENCE_LENGTH),
    LSTM(LSTM_UNITS, return_sequences=True),
    LSTM(LSTM_UNITS),
    Dense(64, activation='relu'),
    Dense(NUM_CLASSES, activation='softmax')  # 다음 코드 예측을 위한 softmax 출력층
])

# 모델 컴파일
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 모델 학습
history = model.fit(X, Y, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.1)

# 모델 저장
model.save("lstm_chord_model.h5")

print("✅ LSTM 모델 학습 완료 및 저장 완료!")