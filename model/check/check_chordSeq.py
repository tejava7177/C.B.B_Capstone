import numpy as np

# 변환된 데이터 로드
chord_sequences = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_sequences.npy", allow_pickle=True)

# 데이터 구조 확인
print("📌 데이터 타입:", type(chord_sequences))
print("📌 배열 차원:", chord_sequences.shape)
print("📌 첫 번째 코드 진행:", chord_sequences[0])