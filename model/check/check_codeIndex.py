import numpy as np

# 코드 매핑 로드
chord_to_index = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy", allow_pickle=True).item()

# 코드 개수 출력
print(f"🎵 현재 코드 개수: {len(chord_to_index)}개")

# 코드 목록 출력
print("📌 현재 코드 리스트:")
for chord in chord_to_index.keys():
    print(chord)