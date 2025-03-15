import tensorflow as tf
import numpy as np
import pretty_midi
from music_transformer_model import MusicTransformer

# ✅ 저장된 모델 로드
model_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/music_transformer_jazz.keras"
model = tf.keras.models.load_model(model_path, custom_objects={"MusicTransformer": MusicTransformer})
print("🎵 모델 로드 완료!")

# ✅ 코드 진행 (4박자 지속)
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


# ✅ 멜로디 & 리듬 생성 함수
def generate_melody_and_rhythm(model, chord_progression, num_steps=4, temperature=1.0):
    generated_melody = []
    generated_rhythm = []

    input_seq = np.zeros((1, 10), dtype=np.int32)
    input_seq[0, -chord_progression.shape[0]:] = chord_progression.flatten()[:10]

    for chord in chord_progression:
        for _ in range(num_steps):
            predicted_probs = model.predict(input_seq, verbose=0)[0, -1, :]

            predicted_probs = np.exp(predicted_probs / temperature)
            predicted_probs /= np.sum(predicted_probs)

            predicted_note = np.random.choice(len(predicted_probs), p=predicted_probs)

            # ✅ 최소한의 음 길이 보장 (0.25~1.0)
            predicted_rhythm = np.random.choice(
                [0.25, 0.5, 0.75, 1.0],
                p=[0.3, 0.3, 0.2, 0.2]
            )

            generated_melody.append(max(0, min(127, predicted_note)))  # ✅ MIDI 범위로 제한
            generated_rhythm.append(predicted_rhythm)

            input_seq = np.roll(input_seq, -1, axis=1)
            input_seq[0, -1] = predicted_note

    return generated_melody, generated_rhythm


# ✅ 🎻 베이스 라인 생성 함수 (워크 베이스 스타일)
def generate_bassline(chord_progression):
    bassline = []
    rhythm = []
    for chord in chord_progression:
        bass_note = max(36, min(127, min(chord) - 12))  # ✅ MIDI 범위 보장
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


# ✅ 멜로디 & 리듬 생성
generated_melody, generated_rhythm = generate_melody_and_rhythm(model, chord_progression)
generated_bassline, bass_rhythm = generate_bassline(chord_progression)
generated_drums, drum_rhythm = generate_drum_pattern(len(chord_progression))


# ✅ MIDI 변환 함수 (여러 트랙 추가)
def create_midi(melody, rhythm, bassline, bass_rhythm, drums, drum_rhythm, output_path="generated_jazz.mid"):
    midi = pretty_midi.PrettyMIDI()

    # 🎹 피아노 멜로디 트랙
    piano = pretty_midi.Instrument(program=0)
    start_time = 0
    for note, duration in zip(melody, rhythm):
        midi_note = pretty_midi.Note(
            velocity=100,
            pitch=max(0, min(127, int(note))),  # ✅ MIDI 범위 제한
            start=start_time,
            end=start_time + max(duration, 0.25)  # ✅ 음 길이 최소 0.25 유지
        )
        piano.notes.append(midi_note)
        start_time += duration
    midi.instruments.append(piano)

    # 🎻 베이스 트랙
    bass = pretty_midi.Instrument(program=32)  # ✅ Acoustic Bass
    start_time = 0
    for note, duration in zip(bassline, bass_rhythm):
        midi_note = pretty_midi.Note(
            velocity=100,
            pitch=max(36, min(127, int(note))),  # ✅ MIDI 범위 제한
            start=start_time,
            end=start_time + max(duration, 0.25)  # ✅ 음 길이 최소 0.25 유지
        )
        bass.notes.append(midi_note)
        start_time += duration
    midi.instruments.append(bass)

    # 🥁 드럼 트랙 (Percussion, Program=128)
    drum = pretty_midi.Instrument(program=128, is_drum=True)
    start_time = 0
    for note, duration in zip(drums, drum_rhythm):
        drum_note = max(35, min(81, int(note)))  # ✅ 드럼 범위 제한 (35~81)
        midi_note = pretty_midi.Note(
            velocity=100,
            pitch=drum_note,
            start=start_time,
            end=start_time + max(duration, 0.25)
        )
        drum.notes.append(midi_note)
        start_time += duration
    midi.instruments.append(drum)

    # ✅ MIDI 저장
    midi.write(output_path)
    print(f"🎼 MIDI 파일 저장 완료: {output_path}")


# ✅ 생성된 멜로디를 MIDI로 변환
create_midi(generated_melody, generated_rhythm, generated_bassline, bass_rhythm, generated_drums, drum_rhythm,
            "generated_jazz.mid")