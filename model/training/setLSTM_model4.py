import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping  # ✅ 조기 종료 추가

# ✅ 기존 코드 인덱스 로드
chord_to_index = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy", allow_pickle=True).item()
NUM_CHORDS = len(chord_to_index)  # ✅ 총 61개 코드 사용

# ✅ 데이터셋 로드
X = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/X.npy")
Y = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/Y.npy")

# ✅ 🔥 Y 데이터를 원-핫 인코딩 변환
Y = to_categorical(Y, num_classes=NUM_CHORDS)

# ✅ LSTM 모델 정의
model = Sequential([
    Embedding(input_dim=NUM_CHORDS, output_dim=64, input_length=3),
    LSTM(128, return_sequences=True),
    LSTM(128),
    Dense(NUM_CHORDS, activation='softmax')
])

# ✅ 모델 컴파일
model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])

# ✅ 학습 설정
EPOCHS = 100  # 🔥 학습 횟수 증가 (기본 50 → 100)
BATCH_SIZE = 256  # 🚀 배치 크기 증가 (128 → 256)

# ✅ 조기 종료 설정 (10번 연속 향상 없으면 종료)
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

print("🚀 모델 학습을 시작합니다...")
model.fit(X, Y, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.2, callbacks=[early_stopping])

# ✅ 모델 저장
MODEL_SAVE_PATH = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/LSTM_model/lstm_chord_model4.h5"
model.save(MODEL_SAVE_PATH)

print(f"✅ 새로운 모델이 저장되었습니다: {MODEL_SAVE_PATH}")