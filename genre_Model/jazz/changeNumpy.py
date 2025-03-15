import json
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ✅ JSON 파일 로드
json_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/jazz_dataset.json"
with open(json_path, "r") as f:
    data = json.load(f)

# ✅ 데이터셋 초기화
X, y = [], []
max_length = 0  # 🚀 최대 시퀀스 길이 저장

# ✅ 데이터 변환
for entry in data["jazz"]:  # 🔥 모든 장르 지원하려면 "jazz" → data.keys() 반복
    chord_seq = entry["chord_progression"]
    melody_seq = entry["melody"]
    rhythm_seq = entry["rhythm_pattern"]

    # 🎵 시퀀스 길이 동기화 (최소 길이로 자르기)
    seq_length = min(len(chord_seq), len(melody_seq), len(rhythm_seq))
    chord_seq, melody_seq, rhythm_seq = chord_seq[:seq_length], melody_seq[:seq_length], rhythm_seq[:seq_length]

    # ✅ 코드 진행이 리스트인지 확인 후 변환 (정수 → 리스트 변환)
    chord_seq = [[note] if isinstance(note, int) else note for note in chord_seq]

    # ✅ 최대 길이 업데이트
    max_length = max(max_length, seq_length)

    # 🎼 입력(X): 현재 코드 진행 + 멜로디 + 리듬 패턴
    input_seq = [chord_seq[i] + [melody_seq[i]["pitch"], rhythm_seq[i]] for i in range(seq_length - 1)]
    if input_seq:  # ✅ 빈 리스트 방지
        X.append(input_seq)

    # 🎼 출력(y): 다음 코드 진행 + 멜로디 예측
    output_seq = [chord_seq[i + 1] + [melody_seq[i + 1]["pitch"]] for i in range(seq_length - 1)]
    if output_seq:  # ✅ 빈 리스트 방지
        y.append(output_seq)

# 🚀 빈 데이터 검증
if not X or not y:
    print("❌ 오류: 데이터가 비어 있습니다. JSON 파일을 확인하세요!")
    exit(1)

# 🚀 패딩 적용하여 길이 맞추기
X_padded = pad_sequences([np.concatenate(x) for x in X], maxlen=max_length, padding="post", dtype="float32")
y_padded = pad_sequences([np.concatenate(y_seq) for y_seq in y], maxlen=max_length, padding="post", dtype="float32")

# ✅ 데이터 정규화 (0~1 범위로 변환)
X_padded = X_padded / 127.0  # MIDI 음표 범위: 0~127
y_padded = y_padded / 127.0

# ✅ NumPy 배열 저장
save_dir = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/"
np.save(save_dir + "X.npy", X_padded)
np.save(save_dir + "y.npy", y_padded)

print(f"✅ 데이터 변환 및 저장 완료! (X: {X_padded.shape}, y: {y_padded.shape})")