import numpy as np

# ✅ 데이터 로드
X = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/X_filtered.npy")
y = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/y_filtered.npy")

# ✅ 샘플링 비율 (예: 10%)
sampling_ratio = 0.1
sample_size = int(len(X) * sampling_ratio)

# ✅ 랜덤 샘플링 (데이터 섞기)
indices = np.random.choice(len(X), sample_size, replace=False)
X_sampled = X[indices]
y_sampled = y[indices]

print(f"✅ 샘플링된 데이터 크기: X = {X_sampled.shape}, y = {y_sampled.shape}")

# ✅ 샘플링된 데이터 저장
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/X_sampled.npy", X_sampled)
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/y_sampled.npy", y_sampled)
print("✅ 데이터 샘플링 완료!")