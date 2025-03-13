import numpy as np
import tensorflow as tf

# 모델 로드
model_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/training/lstm_chord_model4.h5"
model = tf.keras.models.load_model(model_path)

# 코드 매핑 로드
chord_to_index = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy",
                         allow_pickle=True).item()
index_to_chord = {v: k for k, v in chord_to_index.items()}  # 역매핑

# 예측을 위한 설정
SEQUENCE_LENGTH = 4
TEMPERATURE = 1.2  # 🔥 Temperature Sampling 적용


def sample_with_temperature(predictions, temperature=1.5):
    """Temperature Sampling을 적용하여 확률 기반 예측"""
    predictions = np.log(predictions + 1e-8) / temperature
    exp_preds = np.exp(predictions)
    probabilities = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(probabilities), p=probabilities)


# 🎼 새로운 장르 스타일 변환 함수
def apply_style(chord_progression, style="funk"):
    """AI가 예측한 코드 진행을 특정 스타일로 변환"""

    style_map = {
        "punk": {
            "C Major": "C5", "G Major": "G5", "D Major": "D5",
            "A Minor": "A5", "E Minor": "E5", "F Major": "F5",
            "B Major": "B5", "E Major": "E5", "A Major": "A5"
        },
        "reggae": {
            "C Major": "Cmaj7", "G Major": "G7", "D Major": "D7",
            "A Minor": "Am7", "E Minor": "Em7", "F Major": "Fmaj7"
        },
        "rnb": {
            "C Major": "Cmaj9", "G Major": "G9", "D Major": "D9",
            "A Minor": "Am9", "E Minor": "Em9", "F Major": "Fmaj7"
        }
    }

    # 🎯 스타일 맵 적용
    styled_chords = [style_map.get(style, {}).get(chord, chord) for chord in chord_progression]

    # 🎸 코드 변환 최종 조정
    return adjust_chord_progression(styled_chords, style)


def adjust_chord_progression(chords, style):
    """펑크, 레게, R&B 스타일에 맞춰 코드 진행 조정"""
    if style == "punk":
        for i, chord in enumerate(chords):
            if chord.endswith("maj7") or chord.endswith("7") or chord.endswith("9"):
                chords[i] = chord[:-1] + "5"  # ✅ 모든 maj7, 7, 9 코드 → 5 코드 변환
            elif "Minor" in chord or "min" in chord:
                chords[i] = chord.replace("Minor", "5").replace("min", "5")  # ✅ Minor 계열 → 5 코드 변환

    return chords


def predict_next_chords(model, seed_sequence, num_predictions=10, temperature=1.5):
    """주어진 코드 진행에서 다음 코드 예측"""
    predicted_chords = [index_to_chord[idx] for idx in seed_sequence]  # 초기 시퀀스 변환

    for _ in range(num_predictions):
        X_input = np.array([seed_sequence])
        pred = model.predict(X_input, verbose=0)[0]  # 확률값 출력

        next_index = sample_with_temperature(pred, temperature)
        next_chord = index_to_chord[next_index]

        predicted_chords.append(next_chord)
        seed_sequence = seed_sequence[1:] + [next_index]  # 다음 예측을 위해 업데이트

    return predicted_chords


# 🎯 예측 실행 (임의의 초기 코드 진행 설정)
seed_sequence = [chord_to_index["C Major"], chord_to_index["G Major"], chord_to_index["F Minor"], chord_to_index["B Major"]]
predicted_chords = predict_next_chords(model, seed_sequence, num_predictions=12, temperature=TEMPERATURE)

# 🎼 🎸 🎷 🎶 3가지 스타일 변환 적용!
punk_chords = apply_style(predicted_chords, style="punk")
reggae_chords = apply_style(predicted_chords, style="reggae")
rnb_chords = apply_style(predicted_chords, style="rnb")

# 🎼 결과 출력
print("\n🎼 AI가 생성한 원본 코드 진행:")
print(" → ".join(predicted_chords))

print("\n🎵 Punk 스타일 코드 진행:")
print(" → ".join(punk_chords))

print("\n🎶 Reggae 스타일 코드 진행:")
print(" → ".join(reggae_chords))

print("\n🎹 R&B 스타일 코드 진행:")
print(" → ".join(rnb_chords))