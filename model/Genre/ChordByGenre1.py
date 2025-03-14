import numpy as np
import tensorflow as tf

# ✅ 모델 로드
model_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/training/lstm_chord_model4.h5"
model = tf.keras.models.load_model(model_path)

# ✅ 코드 매핑 로드
chord_to_index = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy",
                         allow_pickle=True).item()
index_to_chord = {v: k for k, v in chord_to_index.items()}  # 역매핑

# ✅ 예측을 위한 설정
SEQUENCE_LENGTH = 4
NUM_CHORDS = len(chord_to_index)  # 코드의 총 개수 (ex: 61개)
TEMPERATURE = 1.2  # 🔥 Temperature Sampling 적용


def sample_with_temperature(predictions, temperature=1.5):
    """Temperature Sampling을 적용하여 확률 기반 예측"""
    predictions = np.log(predictions + 1e-8) / temperature
    exp_preds = np.exp(predictions)
    probabilities = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(probabilities), p=probabilities)


def one_hot_encode(sequence, num_classes):
    """입력된 코드 인덱스를 원-핫 인코딩 벡터로 변환"""
    encoded = np.zeros((len(sequence), num_classes))
    for i, index in enumerate(sequence):
        encoded[i, index] = 1  # 해당 코드 위치를 1로 설정
    return encoded


def predict_next_chords(model, seed_sequence, num_predictions=12, temperature=1.5):
    """주어진 코드 진행에서 다음 코드 예측"""
    predicted_chords = [index_to_chord[idx] for idx in seed_sequence]  # 초기 코드 진행 복원

    for _ in range(num_predictions):
        # ✅ 원-핫 인코딩 수행
        X_input = np.expand_dims(one_hot_encode(seed_sequence, NUM_CHORDS), axis=0)  # (1, 4, 61) 형태로 변환

        # ✅ 모델 예측
        pred = model.predict(X_input, verbose=0)[0]  # 확률값 출력

        # ✅ Temperature Sampling 적용
        next_index = sample_with_temperature(pred, temperature)
        next_chord = index_to_chord[next_index]

        predicted_chords.append(next_chord)
        seed_sequence = seed_sequence[1:] + [next_index]  # 시퀀스 업데이트

    return predicted_chords


# 🎼 코드 포맷 정리 함수
def clean_chord_format(chord):
    """공백 제거 및 중복 문자 수정"""
    chord = chord.replace(" ", "")  # 공백 제거
    chord = chord.replace("majmaj", "maj")  # 중복 maj 제거
    chord = chord.replace("minmin", "min")  # 중복 min 제거
    chord = chord.replace("maj7maj7", "maj7")  # 중복 maj7 제거
    return chord


# 🎼 스타일별 코드 진행 변환 (재즈, 블루스, 록 지원)
def apply_style(chord_progression, style="jazz"):
    """AI가 예측한 코드 진행을 특정 스타일로 변환"""
    style_map = {
        "blues": {
            "C Major": "C7", "G Major": "G7", "D Major": "D7",
            "A Major": "A7", "E Major": "E7", "F Major": "F7",
            "B Major": "B7"
        },
        "jazz": {
            "C Major": "Cmaj7", "G Major": "Gmaj7", "D Major": "Dmaj7",
            "A Minor": "Am7", "E Minor": "Em7", "F Major": "Fmaj7",
            "B Minor": "Bm7"
        },
        "rock": {
            "C Major": "C5", "G Major": "G5", "D Major": "D5",
            "A Major": "A5", "E Major": "E5", "F Major": "F5"
        }
    }

    def adjust_chord_progression(chords, style):
        """특정 장르에 맞춰 코드 변환"""
        adjusted_chords = chords[:]  # 원본 유지
        if style == "blues":
            adjusted_chords = [chord.replace("maj7", "7").replace("9", "7") for chord in adjusted_chords]
        elif style == "rock":
            adjusted_chords = [chord.replace("maj7", "5").replace("7", "5").replace("Minor", "5").replace("min", "5")
                               for chord in adjusted_chords]
        elif style == "jazz":
            adjusted_chords = [chord.replace("Major", "maj7") if "Major" in chord else chord for chord in
                               adjusted_chords]

        return adjusted_chords

    styled_chords = [style_map.get(style, {}).get(chord, chord) for chord in chord_progression]

    # ✅ 변환된 코드 포맷 정리
    return [clean_chord_format(chord) for chord in adjust_chord_progression(styled_chords, style)]


# 🎯 예측 실행 (초기 코드 진행 4개 설정)
seed_sequence = [
    chord_to_index["C Major"],
    chord_to_index["G Major"],
    chord_to_index["F Minor"],
    chord_to_index["D Minor"]
]
predicted_chords = predict_next_chords(model, seed_sequence, num_predictions=12, temperature=TEMPERATURE)

# 🎷 **각 장르 스타일로 변환**
jazz_chords = apply_style(predicted_chords, style="jazz")
blues_chords = apply_style(predicted_chords, style="blues")
rock_chords = apply_style(predicted_chords, style="rock")

# 🎼 **결과 출력**
print("\n🎼 AI가 생성한 원본 코드 진행:")
print(" → ".join([clean_chord_format(chord) for chord in predicted_chords]))  # ✅ 공백 문제 해결

print("\n🎷 Jazz 스타일 코드 진행:")
print(" → ".join(jazz_chords))

print("\n🎸 Blues 스타일 코드 진행:")
print(" → ".join(blues_chords))

print("\n🎵 Rock 스타일 코드 진행:")
print(" → ".join(rock_chords))