import numpy as np
import tensorflow as tf
import re

# ✅ 모델 로드
model_path = "/Users/simjuheun/Desktop/myProject/C.B.B/model/training/lstm_chord_model4.h5"
model = tf.keras.models.load_model(model_path)

# ✅ 코드 매핑 로드
chord_to_index = np.load("/Users/simjuheun/Desktop/myProject/C.B.B/model/dataset/chord_to_index.npy",
                         allow_pickle=True).item()
index_to_chord = {v: k for k, v in chord_to_index.items()}  # 역매
# 🎯 AI 예측 설정핑

SEQUENCE_LENGTH = 4
NUM_FEATURES = len(chord_to_index)  # One-hot Encoding을 위한 feature 수
TEMPERATURE = 1.2  # 🔥 Temperature Sampling 적용


def sample_with_temperature(predictions, temperature=1.5):
    """Temperature Sampling을 적용하여 확률 기반 예측"""
    predictions = np.where(predictions == 0, 1e-8, predictions)  # 0값 방지
    predictions = np.log(predictions) / temperature
    exp_preds = np.exp(predictions)
    probabilities = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(probabilities), p=probabilities)


# 🎼 **장르 스타일 변환 함수**
def apply_style(chord_progression, style="punk"):
    """AI가 예측한 코드 진행을 특정 스타일로 변환"""

    style_map = {
        "punk": {
            "C Major": "C5", "G Major": "G5", "D Major": "D5",
            "A Minor": "A5", "E Minor": "E5", "F Major": "F5",
            "B Major": "B5", "E Major": "E5", "A Major": "A5"
        },
        "reggae": {
            "C Major": "Cmaj7", "G Major": "G7", "D Major": "D7",
            "A Minor": "Am7", "E Minor": "Em7", "F Major": "Fmaj7",
            "B Major": "B7", "E Major": "E7", "A Major": "Amaj7"
        },
        "rnb": {
            "C Major": "Cmaj9", "G Major": "G9", "D Major": "D9",
            "A Minor": "Am9", "E Minor": "Em9", "F Major": "Fmaj7",
            "B Major": "Bmaj9", "E Major": "Emaj9", "A Major": "Amaj9"
        }
    }

    styled_chords = [style_map.get(style, {}).get(chord, chord) for chord in chord_progression]
    return adjust_chord_progression(styled_chords, style)


def adjust_chord_progression(chords, style):
    """펑크, 레게, R&B 스타일에 맞춰 코드 진행 조정"""
    adjusted_chords = chords[:]  # 원본 리스트 변형 방지

    if style == "punk":
        for i, chord in enumerate(adjusted_chords):
            if chord.endswith("maj7") or chord.endswith("7") or chord.endswith("9"):
                adjusted_chords[i] = chord[:-1] + "5"  # ✅ 모든 maj7, 7, 9 코드 → 5 코드 변환
            elif "Minor" in chord or "min" in chord:
                adjusted_chords[i] = chord.replace("Minor", "5").replace("min", "5")  # ✅ Minor 계열 → 5 코드 변환

    elif style == "reggae":
        for i, chord in enumerate(adjusted_chords):
            if "Major" in chord and not chord.endswith("7"):
                adjusted_chords[i] = chord.replace("Major", "maj7")  # ✅ 모든 Major → maj7 변환
            elif "Minor" in chord or "min" in chord:
                adjusted_chords[i] = chord.replace("Minor", "m7").replace("min", "m7")  # ✅ Minor 계열 → m7 변환
            elif chord.endswith("7"):
                adjusted_chords[i] = chord.replace("7", "9")  # ✅ 7th 코드 → 9th 변환 (레게 특유 느낌)

    elif style == "rnb":
        for i, chord in enumerate(adjusted_chords):
            if "Major" in chord and not chord.endswith("7"):
                adjusted_chords[i] = chord.replace("Major", "maj9")  # ✅ 모든 Major → maj9 변환
            elif "Minor" in chord or "min" in chord:
                adjusted_chords[i] = chord.replace("Minor", "m9").replace("min", "m9")  # ✅ Minor 계열 → m9 변환
            elif chord.endswith("7"):
                adjusted_chords[i] = chord.replace("7", "maj7")  # ✅ 7th 코드 → maj7 변환 (부드러운 느낌)

    return adjusted_chords


def one_hot_encode(sequence, num_features):
    """주어진 코드 인덱스 시퀀스를 One-Hot Encoding으로 변환"""
    encoded_sequence = np.zeros((len(sequence), num_features))
    for i, index in enumerate(sequence):
        encoded_sequence[i, index] = 1  # 해당 코드 인덱스 위치를 1로 설정
    return encoded_sequence


def predict_next_chords(model, seed_sequence, num_predictions=10, temperature=1.5):
    """주어진 코드 진행에서 다음 코드 예측"""
    predicted_chords = [index_to_chord[idx] for idx in seed_sequence]  # 초기 시퀀스 변환

    for _ in range(num_predictions):
        # ✅ One-Hot Encoding 적용
        X_input = one_hot_encode(seed_sequence, NUM_FEATURES).reshape(1, SEQUENCE_LENGTH, NUM_FEATURES)

        pred = model.predict(X_input, verbose=0)[0]  # 확률값 출력

        next_index = sample_with_temperature(pred, temperature)
        next_chord = index_to_chord[next_index]

        predicted_chords.append(next_chord)
        seed_sequence = seed_sequence[1:] + [next_index]  # 다음 예측을 위해 업데이트

    return predicted_chords

def clean_chord_name(chord):
    """코드명에서 불필요한 공백 제거"""
    return chord.replace(" ", "")  # 모든 공백 제거

def clean_chord_format(chord):
    """코드명에서 불필요한 반복(예: majmaj7 → maj7) 및 형식 오류 정리"""
    chord = re.sub(r'(maj){2,}', 'maj', chord)  # maj가 두 번 이상 반복되면 하나로 축소
    chord = re.sub(r'(min){2,}', 'min', chord)  # min도 같은 방식 적용
    chord = re.sub(r'\s+', '', chord)  # 모든 공백 제거
    return chord


# ✅ **AI 기반 코드 진행 생성**
seed_sequence = [
    chord_to_index["C Major"],
    chord_to_index["G Major"],
    chord_to_index["F Major"],
    chord_to_index["B Major"]
]

predicted_chords = predict_next_chords(model, seed_sequence, num_predictions=12, temperature=TEMPERATURE)

# 🎼 **장르별 스타일 변환 적용**
punk_chords = apply_style(predicted_chords, style="punk")
reggae_chords = apply_style(predicted_chords, style="reggae")
rnb_chords = apply_style(predicted_chords, style="rnb")

# 🎯 코드명 정리 (공백 제거 + 중복 변환 수정)
cleaned_predicted_chords = list(map(lambda chord: clean_chord_format(clean_chord_name(chord)), predicted_chords))
cleaned_punk_chords = list(map(lambda chord: clean_chord_format(clean_chord_name(chord)), punk_chords))
cleaned_reggae_chords = list(map(lambda chord: clean_chord_format(clean_chord_name(chord)), reggae_chords))
cleaned_rnb_chords = list(map(lambda chord: clean_chord_format(clean_chord_name(chord)), rnb_chords))



# 🎼 결과 출력 (정리된 코드 진행)
print("\n🎼 AI가 생성한 원본 코드 진행:")
print(" → ".join(cleaned_predicted_chords))

print("\n🎵 Punk 스타일 코드 진행:")
print(" → ".join(cleaned_punk_chords))

print("\n🎶 Reggae 스타일 코드 진행:")
print(" → ".join(cleaned_reggae_chords))

print("\n🎹 R&B 스타일 코드 진행:")
print(" → ".join(cleaned_rnb_chords))