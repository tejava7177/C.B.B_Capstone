import tensorflow as tf
import numpy as np
import pretty_midi

from music_transformer_model import MusicTransformer

# ✅ 모델 로드
model_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/music_transformer_jazz.keras"
model = tf.keras.models.load_model(model_path, custom_objects={"MusicTransformer": MusicTransformer})
print("🎵 모델 로드 완료!")

# ✅ 코드 진행 (각 코드가 4박자 지속)
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
]
chord_progression = np.array(chord_progression).astype(np.int32)

# ✅ Temperature Sampling 함수
def sample_with_temperature(predictions, temperature=1.2):
    predictions = np.exp(predictions / temperature)
    predictions /= np.sum(predictions)
    return np.random.choice(len(predictions), p=predictions)

# ✅ 멜로디 & 리듬 생성
def generate_melody_and_rhythm(model, chord_progression, sequence_length=32, num_steps=4, temperature=1.2):
    generated_melody = []
    generated_rhythm = []

    input_seq = np.zeros((1, sequence_length), dtype=np.int32)
    input_seq[0, -chord_progression.flatten().shape[0]:] = chord_progression.flatten()[:sequence_length]

    for chord in chord_progression:
        for _ in range(num_steps):
            predicted_probs = model.predict(input_seq, verbose=0)[0, -1, :]
            predicted_note = sample_with_temperature(predicted_probs, temperature)  # ✅ Temperature Sampling 사용

            predicted_note = np.clip(predicted_note, 0, 127)  # ✅ MIDI 범위 강제 적용
            predicted_rhythm = np.random.choice([0.25, 0.5, 0.75, 1.0], p=[0.3, 0.3, 0.2, 0.2])

            generated_melody.append(predicted_note)
            generated_rhythm.append(predicted_rhythm)

            input_seq = np.roll(input_seq, -1, axis=1)
            input_seq[0, -1] = predicted_note

    return generated_melody, generated_rhythm

# ✅ 베이스 라인 생성 (워크 베이스 스타일)
def generate_bassline(chord_progression):
    bassline = []
    rhythm = []
    for chord in chord_progression:
        bass_note = np.clip(min(chord) - 12, 36, 127)  # ✅ MIDI 범위 강제 적용
        bassline.extend([bass_note] * 4)
        rhythm.extend([1.0] * 4)
    return bassline, rhythm

# ✅ 🥁 드럼 패턴 생성 함수 (범위 제한)
def generate_drum_pattern(num_bars=4):
    drum_pattern = []
    rhythm = []
    for _ in range(num_bars):
        drum_hits = [36, 38, 42]  # ✅ (Kick, Snare, HiHat) (값 제한: 35~81)
        drum_pattern.extend(drum_hits)
        rhythm.extend([1.0, 1.0, 0.5])
    return drum_pattern, rhythm

# ✅ 데이터 생성
generated_melody, generated_rhythm = generate_melody_and_rhythm(model, chord_progression)
generated_bassline, bass_rhythm = generate_bassline(chord_progression)
generated_drums, drum_rhythm = generate_drum_pattern(len(chord_progression))


def create_midi(melody, rhythm, bassline, bass_rhythm, drums, drum_rhythm, output_path="generated_jazz.mid"):
    midi = pretty_midi.PrettyMIDI()

    def add_notes_to_instrument(inst, notes, rhythms, min_pitch, max_pitch, is_drum=False):
        start_time = 0
        for note, duration in zip(notes, rhythms):
            int_pitch = int(round(np.clip(note, min_pitch, max_pitch)))  # ✅ 정수 변환
            int_duration = max(float(duration), 0.1)  # ✅ 최소 지속 시간 보장
            int_velocity = int(round(np.clip(100, 1, 127)))  # ✅ 정수 변환

            if int_pitch < 0 or int_pitch > 127:
                print(f"⚠️ 잘못된 pitch 값 발견: {int_pitch}")
            if int_duration <= 0:
                print(f"⚠️ 잘못된 duration 값 발견: {int_duration}")
            if int_velocity < 1 or int_velocity > 127:
                print(f"⚠️ 잘못된 velocity 값 발견: {int_velocity}")

            midi_note = pretty_midi.Note(
                velocity=int_velocity,
                pitch=int_pitch,
                start=start_time,
                end=start_time + int_duration
            )
            inst.notes.append(midi_note)
            start_time += int_duration

    # 🎹 멜로디 트랙
    melody_inst = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
    add_notes_to_instrument(melody_inst, melody, rhythm, 0, 127)
    midi.instruments.append(melody_inst)

    # 🎸 베이스 트랙
    bass_inst = pretty_midi.Instrument(program=32)  # Acoustic Bass
    add_notes_to_instrument(bass_inst, bassline, bass_rhythm, 36, 127)
    midi.instruments.append(bass_inst)

    # 🥁 드럼 트랙
    drum_inst = pretty_midi.Instrument(program=0, is_drum=True)
    add_notes_to_instrument(drum_inst, drums, drum_rhythm, 35, 81)
    midi.instruments.append(drum_inst)

    # ✅ MIDI 저장
    midi.write(output_path)
    print(f"🎼 MIDI 파일 저장 완료: {output_path}")


# ✅ 생성된 MIDI 저장
create_midi(generated_melody, generated_rhythm, generated_bassline, bass_rhythm, generated_drums, drum_rhythm, "generated_jazz.mid")