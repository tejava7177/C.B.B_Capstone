import numpy as np
import os
from data.chord.chord_map import CHORD_MAP  # ✅ 자동으로 코드 리스트 가져오기

# ✅ 파일 경로 설정
CHORD_INDEX_PATH = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy"

# ✅ 기존 코드 매핑 불러오기 (파일이 없으면 새로 생성)
if os.path.exists(CHORD_INDEX_PATH):
    chord_to_index = np.load(CHORD_INDEX_PATH, allow_pickle=True).item()
    print(f"🔍 기존 코드 개수: {len(chord_to_index)}")
else:
    chord_to_index = {}  # 새 파일 생성
    print("⚠️ 기존 코드 매핑 파일이 없음. 새로 생성합니다.")

# ✅ 새로운 코드 목록 자동으로 가져오기
new_chords = set(CHORD_MAP.values())

# ✅ 기존 코드와 비교하여 추가해야 할 코드 찾기
missing_chords = new_chords - set(chord_to_index.keys())

# ✅ 새로운 코드 추가
for chord in missing_chords:
    chord_to_index[chord] = len(chord_to_index)  # 새로운 인덱스 할당

# ✅ 수정된 코드 매핑 저장
np.save(CHORD_INDEX_PATH, chord_to_index)

# ✅ 결과 출력
print(f"✅ 새로운 코드 {len(missing_chords)}개가 추가되었습니다!")
if missing_chords:
    print("🎵 추가된 코드 목록:", missing_chords)
else:
    print("🔹 모든 코드가 이미 등록되어 있습니다.")