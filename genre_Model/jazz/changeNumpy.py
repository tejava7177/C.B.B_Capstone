import json
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ✅ JSON 파일 로드
with open("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/jazz_dataset.json", "r") as f:
    data = json.load(f)

# ✅ 코드 진행, 멜로디, 리듬 패턴 추출
chords, melodies, rhythms = [], [], []

for entry in data["jazz"]:
    chords.append(entry["chords"])
    melodies.append(entry["melody"])
    rhythms.append(entry["rhythm_pattern"])

# ✅ 데이터 패딩 (최대 길이 자동 설정)
max_length = max(max(len(seq) for seq in chords), max(len(seq) for seq in melodies))

chords_padded = pad_sequences(chords, maxlen=max_length, padding="post")
melodies_padded = pad_sequences(melodies, maxlen=max_length, padding="post")
rhythms_padded = pad_sequences(rhythms, maxlen=max_length, padding="post")

# ✅ 데이터 정규화 (0~1 범위로 변환)
chords_padded = chords_padded / 127.0  # MIDI 음표 범위: 0~127
melodies_padded = melodies_padded / 127.0
rhythms_padded = np.array(rhythms_padded)

# ✅ NumPy 배열 저장
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/chords.npy", chords_padded)
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/melodies.npy", melodies_padded)
np.save("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/rhythms.npy", rhythms_padded)

print("🎵 데이터 변환 및 저장 완료! ✅")