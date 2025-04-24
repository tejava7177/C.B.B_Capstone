# 📄 File: model/dataset/normalize_json_chords.py
import os
import json
import numpy as np
import re
from data.chord.chord_to_notes import CHORD_TO_NOTES

# ✅ 디렉토리 생성
os.makedirs("model/dataset", exist_ok=True)

# ✅ 1. JSON 파일 불러오기
json_path = "/Users/simjuheun/Desktop/myProject/C.B.B/model/dataset/midi_chord_data.json"
with open(json_path, "r") as f:
    midi_chord_data = json.load(f)

# ✅ 2. 공백 제거 및 포맷 정규화 함수

def normalize_chord(chord):
    chord = chord.strip()
    chord = chord.replace(" ", "")  # 공백 제거 (예: C Major → CMajor)
    chord = chord.replace("maj", "Maj").replace("min", "Min")
    chord = chord.replace("Major", "Maj").replace("Minor", "Min")
    return chord

# ✅ 3. 모든 코드 정규화 & 필터링
normalized_data = []
all_used_chords = set()

for entry in midi_chord_data:
    new_entry = {}
    chords = entry.get("chords", [])
    norm_chords = [normalize_chord(ch) for ch in chords if normalize_chord(ch) in CHORD_TO_NOTES]
    all_used_chords.update(norm_chords)
    new_entry["chords"] = norm_chords
    if norm_chords:
        normalized_data.append(new_entry)

# ✅ 4. 코드 인덱스 매핑 생성
chord_list = sorted(all_used_chords.union(set(CHORD_TO_NOTES.keys())))
chord_to_index = {ch: i for i, ch in enumerate(chord_list)}
np.save("model/dataset/chord_to_index.npy", chord_to_index)

# ✅ 5. 코드 시퀀스 변환
chord_sequences = [[chord_to_index[ch] for ch in entry["chords"]] for entry in normalized_data]
np.save("model/dataset/chord_sequences.npy", np.array(chord_sequences, dtype=object))

print(f"✅ 정규화된 코드 수: {len(chord_to_index)}개")
print(f"✅ 코드 시퀀스 변환 완료: {len(chord_sequences)}개 진행")
