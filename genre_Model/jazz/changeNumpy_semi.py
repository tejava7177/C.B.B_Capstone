import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ✅ 데이터 로드
X = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/X.npy")
y = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/y.npy")

# ✅ 시퀀스 길이 확인
seq_lengths = [len(seq) for seq in X]
print(f"🔍 데이터셋 내 시퀀스 길이 (최소: {min(seq_lengths)}, 최대: {max(seq_lengths)})")

# ✅ 길이 조정 기준 설정 (중간값 기준으로 조정)
min_seq_length = np.percentile(seq_lengths, 10)  # 하위 10% 제거
max_seq_length = np.percentile(seq_lengths, 90)  # 상위 10% 제거

# ✅ 너무 짧거나 긴 시퀀스 제거
filtered_X = []
filtered_y = []
for i in range(len(X)):
    if min_seq_length <= len(X[i]) <= max_seq_length:
        filtered_X.append(X[i])
        filtered_y.append(y[i])

# ✅ 리스트를 NumPy 배열로 변환
filtered_X = np.array(filtered_X)
filtered_y = np.array(filtered_y)

print(f"✅ 조정 후 데이터 크기: X = {filtered_X.shape}, y = {filtered_y.shape}")

# ✅ NumPy 파일 저장
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/X_filtered.npy", filtered_X)
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/y_filtered.npy", filtered_y)
print("✅ 데이터셋 크기 조정 완료!")