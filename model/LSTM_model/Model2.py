import numpy as np
import tensorflow as tf

# 저장된 모델 로드
MODEL_PATH = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/training/lstm_chord_model.h5"  # 또는 "lstm_chord_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# 코드 매핑 로드
chord_to_index = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy", allow_pickle=True).item()
index_to_chord = {v: k for k, v in chord_to_index.items()}  # 역매핑

# 시퀀스 길이
SEQUENCE_LENGTH = 3

# 🎶 확장된 코드 진행 필터링 규칙 (음악 이론 적용)
VALID_TRANSITIONS = {
    "C Major": ["G Major", "A Minor", "F Major", "E Minor", "Cmaj7", "C7"],
    "G Major": ["C Major", "D Major", "E Minor", "G7", "Gsus4"],
    "A Minor": ["C Major", "F Major", "G Major", "E Minor", "Am7"],
    "F Major": ["C Major", "D Minor", "G Major", "Fmaj7", "Fsus4"],
    "D Minor": ["G Major", "A Minor", "D7", "Dm7", "B Minor"],
    "E Major": ["A Major", "B Major", "C#m", "E7"],
    "B Minor": ["F# Minor", "G Major", "D Major", "Bm7"],
    "Cmaj7": ["Fmaj7", "G7", "A Minor", "C Major"]
}

def sample_with_temperature(predictions, temperature=1.0):
    """Temperature Sampling 적용하여 랜덤성 증가"""
    predictions = np.log(predictions + 1e-9) / temperature  # 확률 분포 조정
    exp_preds = np.exp(predictions)
    probabilities = exp_preds / np.sum(exp_preds)  # 확률값 정규화
    return np.random.choice(len(probabilities), p=probabilities)  # 확률적으로 샘플 선택

def predict_next_chords(model, seed_sequence, num_predictions=10, temperature=1.0):
    """LSTM 모델을 사용하여 더 자연스러운 코드 진행 예측"""
    generated_chords = [index_to_chord[idx] for idx in seed_sequence]

    for _ in range(num_predictions):
        X_input = np.array(seed_sequence).reshape(1, SEQUENCE_LENGTH)
        pred = model.predict(X_input, verbose=0)[0]  # 확률값 출력
        next_chord_idx = sample_with_temperature(pred, temperature)  # Temperature Sampling 적용
        next_chord = index_to_chord[next_chord_idx]

        # 🚨 필터링: 음악 이론에 맞는 코드만 허용
        if generated_chords[-1] in VALID_TRANSITIONS:
            valid_choices = VALID_TRANSITIONS[generated_chords[-1]]
            if next_chord not in valid_choices:
                next_chord = np.random.choice(valid_choices)  # 올바른 코드 중 하나 선택

        generated_chords.append(next_chord)
        seed_sequence = seed_sequence[1:] + [chord_to_index[next_chord]]  # 다음 예측을 위해 업데이트

    return generated_chords

# 예제 코드 진행 (C Major → G Major → A Minor)
seed_sequence = [chord_to_index["C Major"], chord_to_index["G Major"], chord_to_index["A Minor"]]

# Temperature=1.2로 설정하여 랜덤성 증가
predicted_chords = predict_next_chords(model, seed_sequence, num_predictions=10, temperature=1.2)

print("🎼 AI가 생성한 개선된 코드 진행:")
print(" → ".join(predicted_chords))