import numpy as np

# 로드
chord_to_index = np.load("/Users/simjuheun/Desktop/myProject/C.B.B/model/dataset/model/dataset/chord_to_index.npy", allow_pickle=True).item()

# 정렬된 코드명 목록 출력
sorted_chords = sorted(chord_to_index.keys())
print(f"🎼 총 {len(sorted_chords)}개 코드:")
for chord in sorted_chords:
    print("-", chord)