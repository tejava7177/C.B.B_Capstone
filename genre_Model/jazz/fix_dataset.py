import numpy as np

# ✅ 기존 데이터 로드
dataset_dir = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/"
X_old = np.load(dataset_dir + "X.npy")
y_old = np.load(dataset_dir + "y.npy")

# ✅ 새로운 sequence_length 설정
sequence_length = 32  # 또는 64

# ✅ 새로운 데이터셋 생성
X_new = []
y_new = []
for i in range(len(X_old) - sequence_length):
    X_new.append(X_old[i:i+sequence_length])
    y_new.append(y_old[i:i+sequence_length])

X_new = np.array(X_new)
y_new = np.array(y_new)

# ✅ 저장
np.save(dataset_dir + "X_new.npy", X_new)
np.save(dataset_dir + "y_new.npy", y_new)

print(f"✅ 데이터셋 변환 완료! 새로운 X.shape: {X_new.shape}, y.shape: {y_new.shape}")
