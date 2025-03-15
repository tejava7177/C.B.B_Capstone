import tensorflow as tf
import numpy as np
import pretty_midi
from music_transformer_model import MusicTransformer

# ✅ 저장된 모델 로드
model_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/music_transformer_jazz.keras"
model = tf.keras.models.load_model(model_path, custom_objects={"MusicTransformer": MusicTransformer})
print("🎵 모델 로드 완료!")

# ✅ 주어진 코드 진행
chord_progression = [
    [60, 64, 67],  # Cmaj7
    [67, 71, 74],  # Gmaj7
    [65, 68, 72],  # Fm
    [62, 65, 69],  # Dm
    [67, 71, 74],  # Gmaj7
    [71, 74, 77],  # Bdim
    [71, 75, 79],  # Bmaj7
    [64, 68, 72],  # Emaj7
    [71, 74, 77],  # Bdim
    [65, 69, 72],  # Fsus4
    [71, 75, 79]  # Bmaj7
]
chord_progression = np.array(chord_progression).astype(np.int32)


# ✅ 멜로디 & 리듬 생성 함수 (입력 차원 변환 + softmax 안정화)
def generate_melody_and_rhythm(model, chord_progression, temperature=1.0):
    generated_melody = []
    generated_rhythm = []

    for chord in chord_progression:
        input_seq = np.expand_dims(chord, axis=0)  # (3,) -> (1, 3)
        predicted_probs = model.predict(input_seq, verbose=0)[0, -1, :]  # 마지막 step 예측

        # 🔥 Temperature Sampling 적용 (softmax 변환)
        predicted_probs = np.exp(predicted_probs / temperature)  # 확률 조정
        predicted_probs /= np.sum(predicted_probs)  # 정규화 (확률 분포)

        predicted_note = np.random.choice(len(predicted_probs), p=predicted_probs)
        predicted_rhythm = np.random.choice([0.25, 0.5, 1, 2], p=[0.3, 0.3, 0.3, 0.1])  # 🎵 랜덤 리듬

        generated_melody.append(predicted_note)
        generated_rhythm.append(predicted_rhythm)

    return generated_melody, generated_rhythm


# ✅ 멜로디 & 리듬 생성
generated_melody, generated_rhythm = generate_melody_and_rhythm(model, chord_progression)

# ✅ 생성된 멜로디 & 리듬 출력
print("🎶 생성된 멜로디:", generated_melody)
print("🥁 생성된 리듬:", generated_rhythm)


# ✅ MIDI 변환 함수 (노트 범위 조정)
def create_midi(melody, rhythm, output_path="generated_jazz.mid"):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    start_time = 0
    for note, duration in zip(melody, rhythm):
        midi_note = pretty_midi.Note(
            velocity=100,
            pitch=max(0, min(127, int(note))),  # MIDI 범위 내에서 제한
            start=start_time,
            end=start_time + duration
        )
        instrument.notes.append(midi_note)
        start_time += duration

    midi.instruments.append(instrument)
    midi.write(output_path)
    print(f"🎼 MIDI 파일 저장 완료: {output_path}")


# ✅ 생성된 멜로디를 MIDI로 변환
create_midi(generated_melody, generated_rhythm, "generated_jazz.mid")