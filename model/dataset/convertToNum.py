import numpy as np
import json

# 코드 매핑 로드
with open("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/midi_chord_data.json", "r") as f:
    midi_chord_data = json.load(f)

# 고유 코드 리스트 생성
unique_chords = sorted(set(chord for entry in midi_chord_data for chord in entry["chords"]))

# 코드 -> 숫자 매핑
chord_to_index = {chord: i for i, chord in enumerate(unique_chords)}
index_to_chord = {i: chord for chord, i in chord_to_index.items()}

# 코드 진행을 숫자로 변환
chord_sequences = [[chord_to_index[chord] for chord in entry["chords"]] for entry in midi_chord_data]

# 변환된 데이터 저장
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_sequences.npy", np.array(chord_sequences, dtype=object))
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy", chord_to_index)

print(f"✅ 코드 진행 데이터를 숫자로 변환 완료! (총 {len(chord_sequences)}개)")
print(f"🎵 고유 코드 개수: {len(chord_to_index)}개")