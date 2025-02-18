import numpy as np

# 기존 코드 매핑 로드
chord_to_index = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy", allow_pickle=True).item()

# 새로운 코드 목록
new_chords = [
    # Seventh Chords (7th 코드)
    "Cmaj7", "Gmaj7", "Amaj7", "Dmaj7", "Emaj7", "Fmaj7", "Bmaj7",
    "C7", "G7", "A7", "D7", "E7", "B7", "F7",

    # Suspended Chords (서스펜디드 코드)
    "Csus4", "Gsus4", "Asus4", "Dsus4", "Esus4", "Fsus4",

    # Diminished Chords (디미니쉬 코드)
    "Cdim", "Gdim", "Adim", "Ddim", "Bdim",

    # Augmented Chords (어그먼트 코드)
    "Caug", "Gaug", "Aaug", "Daug"
]

# 새로운 코드 추가
for chord in new_chords:
    if chord not in chord_to_index:
        chord_to_index[chord] = len(chord_to_index)  # 새로운 인덱스 할당

# 수정된 코드 매핑 저장
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy", chord_to_index)

print("✅ 새로운 코드가 추가되었습니다!")