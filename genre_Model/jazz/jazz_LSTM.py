import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# ✅ 1. 데이터 로드
chords = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/chords.npy")
melodies = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/melodies.npy")
rhythms = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/rhythms.npy")

# ✅ 2. 데이터 전처리 (입력/출력 분리)
X = np.concatenate((chords, melodies, rhythms), axis=1)  # 코드, 멜로디, 리듬 결합
y = np.concatenate((chords[:, :X.shape[1]], melodies[:, :X.shape[1]], rhythms[:, :X.shape[1]]), axis=1)  # 🚀 X와 같은 길이 유지

# ✅ 3. 차원 확인 및 변환
print("📏 원본 데이터 차원:", X.shape)
if len(X.shape) == 2:
    X = np.expand_dims(X, axis=-1)  # (샘플 개수, 시퀀스 길이, 1)로 변환

print("📏 변환된 데이터 차원:", X.shape)

# ✅ 4. y를 LSTM 출력 차원과 맞춤
y = tf.keras.utils.to_categorical(y, num_classes=128)  # MIDI 음표 개수에 맞게 변환
print("📏 변환된 y 데이터 차원:", y.shape)  # 🚀 (25225, 30, 128)로 일치해야 함

# ✅ 5. LSTM 모델 설계
model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
    Dropout(0.3),
    LSTM(64, return_sequences=True),
    Dropout(0.3),
    Dense(y.shape[2], activation="softmax")  # 🚀 수정된 부분
])

# ✅ 6. 모델 컴파일
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# ✅ 7. 모델 학습
model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)

# ✅ 8. 모델 저장
model.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/lstm_jazz_model.h5")

print("🎵 LSTM 모델 학습 및 저장 완료! ✅")