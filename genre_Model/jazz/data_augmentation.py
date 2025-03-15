import numpy as np
import os

# ✅ 데이터 로드
dataset_dir = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/"
X = np.load(os.path.join(dataset_dir, "X.npy"))
y = np.load(os.path.join(dataset_dir, "y.npy"))

# ✅ 전조 변환 (Transpose)
transposed_X = []
transposed_y = []

transpose_intervals = [-2, -1, 0, 1, 2]  # -2, -1, 원본, +1, +2

for interval in transpose_intervals:
    new_X = X + interval
    new_y = y + interval
    new_X = np.clip(new_X, 0, 127)  # MIDI 범위 제한
    new_y = np.clip(new_y, 0, 127)
    transposed_X.append(new_X)
    transposed_y.append(new_y)

# ✅ 변환된 데이터 저장
augmented_X = np.concatenate(transposed_X, axis=0)
augmented_y = np.concatenate(transposed_y, axis=0)

np.save(os.path.join(dataset_dir, "X_augmented.npy"), augmented_X)
np.save(os.path.join(dataset_dir, "y_augmented.npy"), augmented_y)

print("✅ 데이터 증강 완료: X_augmented.npy, y_augmented.npy 생성")
