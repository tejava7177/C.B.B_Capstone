# 📄 File: model/dataset/build_XY.py

import numpy as np
from tensorflow.keras.utils import to_categorical
import os

# ✅ 경로 설정
base_dir = "model/dataset"
chord_sequences_path = os.path.join(base_dir, "chord_sequences.npy")
chord_to_index_path = os.path.join(base_dir, "chord_to_index.npy")

# ✅ 데이터 로드
chord_sequences = np.load(chord_sequences_path, allow_pickle=True)
chord_to_index = np.load(chord_to_index_path, allow_pickle=True).item()

SEQUENCE_LENGTH = 4
NUM_CLASSES = len(chord_to_index)

# ✅ X, Y 데이터 생성
X, Y = [], []

for seq in chord_sequences:
    for i in range(len(seq) - SEQUENCE_LENGTH):
        X.append(seq[i:i+SEQUENCE_LENGTH])
        Y.append(seq[i+SEQUENCE_LENGTH])

X = np.array(X)
Y = np.array(Y)

# ✅ One-Hot Encoding 적용
Y = to_categorical(Y, num_classes=NUM_CLASSES)

# ✅ 저장
np.save(os.path.join(base_dir, "X.npy"), X)
np.save(os.path.join(base_dir, "Y.npy"), Y)

print(f"✅ X, Y 데이터 저장 완료!")
print(f"🔹 X.shape = {X.shape}")
print(f"🔹 Y.shape = {Y.shape}")
