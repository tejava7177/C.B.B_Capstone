import numpy as np
import pretty_midi
from keras.models import load_model
import sys

# 📌 chord_to_notes.py 파일에서 코드 노트 매핑 가져오기
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord/")
from chord_to_notes import CHORD_TO_NOTES  # 🔥 코드 진행을 노트 리스트로 변환

# 📌 모델 파일 경로 설정
model_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/lstm_jazz_model.h5"

# ✅ 모델 불러오기
try:
    model = load_model(model_path)
    print(f"✅ 모델 로드 완료: {model_path}")
except FileNotFoundError:
    print(f"❌ 오류: 모델 파일을 찾을 수 없습니다! 경로를 확인해주세요: {model_path}")
    exit(1)


# 🎼 **재즈 스타일 MIDI 생성 (사용자 지정 코드 진행)**
def generate_jazz_midi(model, chord_progression, output_length=50):
    """사용자가 지정한 코드 진행을 기반으로 다중 악기 포함 MIDI 생성"""
    generated_chords = []  # 🎹 피아노 코드 진행
    generated_melody = []  # 🎷 색소폰 멜로디 추가
    generated_bass = []  # 🎸 베이스 음 추가

    # 📌 코드 진행을 MIDI 노트 리스트로 변환
    for chord in chord_progression:
        if chord in CHORD_TO_NOTES:
            generated_chords.extend(CHORD_TO_NOTES[chord])
        else:
            print(f"⚠️ 경고: {chord} 코드가 CHORD_TO_NOTES 없음! 기본 CMajor 사용")
            generated_chords.extend(CHORD_TO_NOTES["CMajor"])

    # 📌 모델을 사용하여 멜로디 예측
    for _ in range(output_length):
        if len(generated_chords) < 30:
            generated_chords.extend(CHORD_TO_NOTES["CMajor"])  # 최소 길이 보장
        input_seq = np.array(generated_chords[-30:]).reshape(1, 30, 1)
        prediction = model.predict(input_seq)
        next_note = np.argmax(prediction)

        # 📌 MIDI 범위 초과 방지 (0~127 사이로 제한)
        next_note = max(50, min(next_note, 80))

        # 🎷 색소폰 멜로디 추가 (랜덤 변형)
        melody_note = next_note + np.random.choice([-2, 3, 5])
        melody_note = max(50, min(melody_note, 80))
        generated_melody.append(melody_note)

        # 🎸 베이스 루트 음 추가 (코드 첫 번째 음)
        bass_note = max(30, min(generated_chords[-1] - 24, 60))
        generated_bass.append(bass_note)

    # 🎵 MIDI 파일 생성
    midi = pretty_midi.PrettyMIDI()

    # 🎹 피아노 코드 진행 추가
    piano = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
    start_time = 0
    for note in generated_chords:
        midi_note = pretty_midi.Note(velocity=100, pitch=note, start=start_time, end=start_time + 1.0)
        piano.notes.append(midi_note)
        start_time += 1.0
    midi.instruments.append(piano)

    # 🎸 베이스 트랙 추가
    bass = pretty_midi.Instrument(program=33)  # Acoustic Bass
    start_time = 0
    for note in generated_bass:
        midi_note = pretty_midi.Note(velocity=90, pitch=note, start=start_time, end=start_time + 1.0)
        bass.notes.append(midi_note)
        start_time += 1.0
    midi.instruments.append(bass)

    # 🎷 색소폰 멜로디 트랙 추가
    sax = pretty_midi.Instrument(program=65)  # Alto Sax
    start_time = 0
    for note in generated_melody:
        midi_note = pretty_midi.Note(velocity=110, pitch=note, start=start_time, end=start_time + 0.7)
        sax.notes.append(midi_note)
        start_time += 0.7
    midi.instruments.append(sax)

    # 🥁 드럼 비트 추가 (스윙 리듬 적용)
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    start_time = 0
    for _ in range(output_length):
        if start_time % 2.0 == 0:  # 🎵 킥 드럼 (기본 박자)
            kick = pretty_midi.Note(velocity=100, pitch=36, start=start_time, end=start_time + 0.2)
            drums.notes.append(kick)
        if start_time % 1.0 == 0:  # 🎵 스네어 드럼
            snare = pretty_midi.Note(velocity=100, pitch=38, start=start_time, end=start_time + 0.2)
            drums.notes.append(snare)
        if start_time % 0.5 == 0:  # 🎶 하이햇
            hihat = pretty_midi.Note(velocity=80, pitch=42, start=start_time, end=start_time + 0.1)
            drums.notes.append(hihat)
        start_time += 0.5
    midi.instruments.append(drums)

    # ✅ MIDI 파일 저장
    midi_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/generated_jazz_chords.mid"
    midi.write(midi_path)
    print(f"🎶 재즈 코드 진행 MIDI 파일 저장 완료: {midi_path}")


# 📌 사용자가 원하는 코드 진행
user_chord_progression = [
    "Cmaj7", "Gmaj7", "FMinor", "DMinor", "Cmaj7", "Gmaj7", "Caug", "A7"
]

generate_jazz_midi(model, user_chord_progression)