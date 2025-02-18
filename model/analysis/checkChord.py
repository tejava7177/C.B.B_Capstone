import numpy as np

# 저장된 코드 매핑 로드
chord_to_index = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy", allow_pickle=True).item()

# 모든 코드 출력
print("🎵 현재 코드 리스트:")
for chord in chord_to_index.keys():
    print(chord)

# 특정 코드 확인
if "Cmaj7" in chord_to_index:
    print("✅ 'Cmaj7' 코드가 존재합니다.")
else:
    print("🚨 'Cmaj7' 코드가 없습니다. 추가가 필요합니다.")