import numpy as np
from tensorflow.keras.utils import to_categorical

# 데이터 로드
chord_sequences = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_sequences.npy", allow_pickle=True)
chord_to_index = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy", allow_pickle=True).item()

# 하이퍼파라미터 설정
SEQUENCE_LENGTH = 4  # 코드 진행 예측을 위한 입력 길이
NUM_CLASSES = len(chord_to_index)  # 🔥 총 코드 개수 반영

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

# 데이터 저장
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/X.npy", X)
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/Y.npy", Y)

print(f"✅ 데이터셋 준비 완료! (X: {X.shape}, Y: {Y.shape})")