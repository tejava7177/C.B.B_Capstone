import numpy as np
import json

# 코드 매핑 로드
chord_to_index = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy", allow_pickle=True).item()

# MIDI 코드 진행 데이터 로드
with open("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/midi_chord_data.json", "r") as f:
    midi_chord_data = json.load(f)

# 코드 진행을 숫자로 변환
chord_sequences = []
for entry in midi_chord_data:
    chord_sequence = [chord_to_index.get(chord, -1) for chord in entry["chords"]]  # 없는 코드는 -1 처리
    chord_sequences.append(chord_sequence)

# 숫자로 변환된 데이터 저장
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_sequences.npy", np.array(chord_sequences, dtype=object))

print("✅ 코드 진행 데이터를 숫자로 변환 완료!")