import numpy as np

# 변환된 데이터 로드
X = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/X.npy")
Y = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/Y.npy")

# 데이터 구조 확인
print("📌 X 데이터 차원:", X.shape)
print("📌 Y 데이터 차원:", Y.shape)
print("📌 Y 데이터 타입:", Y.dtype)

# ✅ 첫 번째 샘플 데이터 출력
print("📌 첫 번째 입력 시퀀스 (X):", X[0])
print("📌 첫 번째 출력 코드 (One-Hot) (Y):", Y[0])

# ✅ Y 데이터의 최소/최대 값 확인 (One-Hot Encoding인지 확인)
print("📌 Y 데이터 최소값:", np.min(Y))
print("📌 Y 데이터 최대값:", np.max(Y))

# ✅ Y 데이터 차원 분석
print("📌 Y 데이터 shape (axis별):", [Y.shape[i] for i in range(len(Y.shape))])

# ✅ Y 데이터 내부 값 예제 (5개 출력)
for i in range(5):
    print(f"📌 Y[{i}] 샘플:", Y[i])