import numpy as np
from tensorflow.keras.utils import to_categorical

# 데이터 로드
chord_sequences = np.load("chord_sequences.npy")
chord_to_index = np.load("chord_to_index.npy", allow_pickle=True).item()
index_to_chord = {v: k for k, v in chord_to_index.items()}  # 역매핑

# 하이퍼파라미터 설정
SEQUENCE_LENGTH = 3  # LSTM이 이전 몇 개의 코드를 보고 다음 코드 예측할지 결정
NUM_CLASSES = len(chord_to_index)  # 코드의 총 개수

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