import json
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

# JSON 파일 로드
input_json_path = "midi_chord_data.json"
with open(input_json_path, "r") as f:
    midi_chord_data = json.load(f)

# 모든 코드 추출하여 고유 인덱스 부여
unique_chords = sorted(set(chord for entry in midi_chord_data for chord in entry["chords"]))
chord_to_index = {chord: idx for idx, chord in enumerate(unique_chords)}
index_to_chord = {idx: chord for chord, idx in chord_to_index.items()}

# 코드 진행을 숫자로 변환
numeric_sequences = [[chord_to_index[chord] for chord in entry["chords"]] for entry in midi_chord_data]

# LSTM 모델을 위해 시퀀스 길이 맞추기 (최대 길이 설정)
MAX_SEQUENCE_LENGTH = 16  # 너무 긴 코드 진행은 자르고, 짧은 것은 패딩
padded_sequences = pad_sequences(numeric_sequences, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post")

# 변환된 데이터를 numpy 배열로 저장
np.save("chord_sequences.npy", padded_sequences)
np.save("chord_to_index.npy", chord_to_index)

print(f"✅ 코드 진행 데이터를 숫자로 변환 완료! (총 {len(padded_sequences)}개)")
print(f"🎵 고유 코드 개수: {len(chord_to_index)}개")