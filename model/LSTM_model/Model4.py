import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical

# ✅ 모델 로드
model_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/training/lstm_chord_model4.h5"
model = tf.keras.models.load_model(model_path)

# ✅ 코드 매핑 로드
chord_to_index = np.load("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/chord_to_index.npy",
                         allow_pickle=True).item()
index_to_chord = {v: k for k, v in chord_to_index.items()}  # 역매핑

# ✅ 예측을 위한 설정
SEQUENCE_LENGTH = 4  # ✅ 모델이 기대하는 입력 크기로 설정
NUM_CHORDS = len(chord_to_index)  # ✅ 코드 개수 (61개)
TEMPERATURE = 1.2  # 🔥 Temperature Sampling 적용


def sample_with_temperature(predictions, temperature=1.5):
    """Temperature Sampling을 적용하여 확률 기반 예측"""
    predictions = np.log(predictions + 1e-8) / temperature
    exp_preds = np.exp(predictions)
    probabilities = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(probabilities), p=probabilities)


def predict_next_chords(model, seed_sequence, num_predictions=10, temperature=1.5):
    """주어진 코드 진행에서 다음 코드 예측"""
    predicted_chords = [index_to_chord[idx] for idx in seed_sequence]  # 초기 시퀀스 변환

    for _ in range(num_predictions):
        seed_sequence = seed_sequence[-SEQUENCE_LENGTH:]  # ✅ 항상 입력 크기 맞추기

        # ✅ One-Hot Encoding 변환 (모델 입력 형태 맞추기)
        X_input = np.array([seed_sequence])  # shape: (1, SEQUENCE_LENGTH)
        X_input = to_categorical(X_input, num_classes=NUM_CHORDS)  # shape: (1, SEQUENCE_LENGTH, 61)

        pred = model.predict(X_input, verbose=0)[0]  # 확률값 출력
        next_index = sample_with_temperature(pred, temperature)

        if next_index not in index_to_chord:
            print(f"⚠️ Warning: 예상 범위를 벗어난 코드 인덱스 {next_index}, 기본 코드 사용")
            next_index = 0  # 기본값으로 C Major

        next_chord = index_to_chord[next_index]
        predicted_chords.append(next_chord)
        seed_sequence.append(next_index)  # ✅ 새로운 코드 추가

    return predicted_chords


# ✅ 예측 실행 (임의의 초기 코드 진행 설정)
seed_sequence = [chord_to_index["Cmaj7"], chord_to_index["Fmaj7"], chord_to_index["Cmaj7"], chord_to_index["Gm7"]]
predicted_chords = predict_next_chords(model, seed_sequence, num_predictions=12, temperature=TEMPERATURE)

# ✅ 결과 출력
print("🎼 AI가 생성한 코드 진행:")
print(" → ".join(predicted_chords))