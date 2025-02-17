import numpy as np
import tensorflow as tf

# 저장된 모델 로드 (h5 또는 keras 중 선택 가능)
MODEL_PATH = "lstm_chord_model.h5"  # "lstm_chord_model.h5"도 가능
model = tf.keras.models.load_model(MODEL_PATH)

# 저장된 코드 매핑 로드
chord_to_index = np.load("chord_to_index.npy", allow_pickle=True).item()
index_to_chord = {v: k for k, v in chord_to_index.items()}  # 역매핑

# 예측을 위한 입력 시퀀스 길이
SEQUENCE_LENGTH = 3

def predict_next_chords(model, seed_sequence, num_predictions=5):
    """LSTM 모델을 사용하여 다음 코드 진행 예측"""
    generated_chords = [index_to_chord[idx] for idx in seed_sequence]  # 초기 코드 진행

    for _ in range(num_predictions):
        X_input = np.array(seed_sequence).reshape(1, SEQUENCE_LENGTH)  # 모델 입력 형식 변환
        pred = model.predict(X_input, verbose=0)
        next_chord_idx = np.argmax(pred)  # 확률이 가장 높은 코드 선택
        next_chord = index_to_chord[next_chord_idx]

        generated_chords.append(next_chord)
        seed_sequence = seed_sequence[1:] + [next_chord_idx]  # 다음 예측을 위해 업데이트

    return generated_chords


# # 코드 진행 출력 1
# # 예제 코드 진행 (C Major → G Major → A Minor)
# seed_sequence = [chord_to_index["C Major"], chord_to_index["G Major"], chord_to_index["A Minor"]]
#
#
# # 10개의 코드 예측
# predicted_chords = predict_next_chords(model, seed_sequence, num_predictions=10)
#
# print("🎼 AI가 생성한 코드 진행:")
# print(" → ".join(predicted_chords))


# 예제 2: 다른 코드 진행으로 예측 테스트
seed_sequence = [chord_to_index["D Minor"], chord_to_index["A Minor"], chord_to_index["E Major"]]
predicted_chords = predict_next_chords(model, seed_sequence, num_predictions=10)

print("🎼 새로운 코드 진행 예측 결과:")
print(" → ".join(predicted_chords))