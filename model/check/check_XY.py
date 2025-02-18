import numpy as np

# 변환된 데이터 로드
X = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/X.npy")
Y = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/Y.npy")

# 데이터 구조 확인
print("📌 X 데이터 차원:", X.shape)
print("📌 Y 데이터 차원:", Y.shape)

# 일부 데이터 출력
print("📌 첫 번째 입력 시퀀스:", X[0])
print("📌 첫 번째 출력 코드 (One-Hot):", Y[0])