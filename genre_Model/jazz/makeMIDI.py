import numpy as np
import pretty_midi
import random
from keras.models import load_model
import sys

sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord/")
from chord_to_notes import CHORD_TO_NOTES

# 📌 모델 로드
model_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/lstm_jazz_model.h5"
model = load_model(model_path)
print(f"✅ 모델 로드 완료: {model_path}")

# 🎼 **재즈 스타일 MIDI 생성 (오류 방지 적용)**
def generate_jazz_midi(model, chord_progression, output_length=50):
    """재즈 스타일의 MIDI 파일을 생성 (스윙 리듬, 워킹 베이스, 즉흥 멜로디 포함)"""
    generated_chords, generated_melody, generated_bass = [], [], []

    # ✅ 코드 진행을 재즈 보이싱 스타일로 변형하여 저장
    for chord in chord_progression:
        if chord in CHORD_TO_NOTES:
            notes = CHORD_TO_NOTES[chord]
            jazz_voicing = [notes[0], notes[1] + 2, notes[2] + 5]  # 루트 위치 변경 (보이싱 적용)
            generated_chords.extend(jazz_voicing)
        else:
            generated_chords.extend(CHORD_TO_NOTES["CMajor"])

    # ✅ 최소 30개 이상 확보 (부족한 경우 앞에서 반복 추가)
    while len(generated_chords) < 30:
        generated_chords = generated_chords + generated_chords[:30 - len(generated_chords)]

    # ✅ 모델을 사용하여 즉흥적 멜로디 예측 (스윙 리듬 적용)
    for _ in range(output_length):
        input_seq = np.array(generated_chords[-30:]).reshape(1, 30, 1)  # 🔥 reshape 오류 방지
        prediction = model.predict(input_seq)
        next_note = np.argmax(prediction)
        next_note = max(50, min(next_note, 80))  # MIDI 범위 제한

        # 🎷 재즈 스케일 기반 멜로디 변형
        melody_note = next_note + np.random.choice([-2, 3, 5])
        melody_note = max(50, min(melody_note, 85))
        generated_melody.append(melody_note)

        # 🎸 워킹 베이스 라인 생성
        bass_note = max(30, min(generated_chords[-1] - np.random.choice([12, 7, 5]), 60))
        generated_bass.append(bass_note)

    # 🎵 MIDI 파일 생성
    midi = pretty_midi.PrettyMIDI()

    # 🎹 피아노 코드 트랙 (재즈적인 보이싱 & 리듬 추가)
    piano = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    start_time = 0
    for chord in chord_progression:
        if chord in CHORD_TO_NOTES:
            root = CHORD_TO_NOTES[chord][0]  # 루트음
            third = CHORD_TO_NOTES[chord][1]  # 3rd
            fifth = CHORD_TO_NOTES[chord][2]  # 5th

            # 🔥 텐션 코드 추가 (재즈적인 사운드 강화)
            seventh = root + 10 if root + 10 <= 80 else root + 7
            ninth = root + 14 if root + 14 <= 84 else root + 12

            # ✅ 재즈 보이싱 구성 (Open Voicing & Tension)
            jazz_chord = [root, third, seventh, ninth]

            # 🎵 스윙 리듬 적용 (8분음표 & 16분음표 조합)
            for i, note in enumerate(jazz_chord):
                velocity = random.randint(70, 110)  # 연주 강도 랜덤화
                note_length = 0.5 if i % 2 == 0 else 0.25  # 일부 음은 짧게 처리

                # 🎶 음이 너무 높거나 낮으면 자동 조정
                note = max(48, min(note, 84))

                midi_note = pretty_midi.Note(velocity=velocity, pitch=note, start=start_time,
                                             end=start_time + note_length)
                piano.notes.append(midi_note)
                start_time += note_length  # 리듬 패턴 반영

    # 🎹 피아노 트랙 추가
    midi.instruments.append(piano)

    # 🎸 Electric Bass (finger) 트랙 (데이터셋 기반 + 랜덤 연주)
    bass = pretty_midi.Instrument(program=33)  # Electric Bass (finger)

    start_time = 0
    for i, chord in enumerate(chord_progression):
        if chord in CHORD_TO_NOTES:
            root = CHORD_TO_NOTES[chord][0]  # 루트음
            third = CHORD_TO_NOTES[chord][1]  # 3rd
            fifth = CHORD_TO_NOTES[chord][2]  # 5th
            octave = root + 12 if root + 12 <= 62 else root  # 한 옥타브 위 추가

            # ✅ 데이터셋 기반 음역대 및 벨로시티 설정
            dataset_bass_range = (30, 50)  # 데이터셋에서 일반적으로 사용되는 음역대
            dataset_velocity_range = (60, 110)  # 데이터셋에서 사용된 벨로시티 범위

            # 🎶 베이스 진행 패턴 (루트 → 3rd → 5th → 옥타브)
            bass_notes = [root, third, fifth, octave]  # 🔥 문제 해결: 실제 코드 진행 반영!

            # 🔥 크로매틱 접근음 추가 (다음 코드 루트로 반음 접근)
            if i < len(chord_progression) - 1:
                next_root = CHORD_TO_NOTES[chord_progression[i + 1]][0] if chord_progression[
                                                                               i + 1] in CHORD_TO_NOTES else root
                approach_note = next_root - 1 if next_root - 1 >= dataset_bass_range[0] else next_root + 1  # 반음 접근음 추가
                bass_notes.append(approach_note)

            # 🎵 리듬 패턴 설정 (8분, 16분 혼합 + 스타카토 느낌 적용)
            note_lengths = [0.5, 0.25, 0.75]  # 8분 & 16분 혼합 리듬
            for j in range(len(bass_notes)):  # 🔥 문제 해결: 실제 bass_notes 리스트의 모든 노트 사용
                note = bass_notes[j]  # ✅ 리스트에서 순차적으로 가져오기

                # ✅ 음역대 조정 (데이터셋 범위 내에서 유지)
                note = max(dataset_bass_range[0], min(note, dataset_bass_range[1]))

                # ✅ Velocity 조정 (데이터셋 범위 기반)
                velocity = random.randint(dataset_velocity_range[0], dataset_velocity_range[1])

                # 🎼 리듬 변형 (랜덤 길이 적용)
                note_length = random.choice(note_lengths)

                midi_note = pretty_midi.Note(velocity=velocity, pitch=note, start=start_time,
                                             end=start_time + note_length)
                bass.notes.append(midi_note)

                start_time += note_length  # ✅ 다음 노트로 이동 (연속적인 진행 보장)

    # 🎸 베이스 트랙 추가
    midi.instruments.append(bass)

    # 🎷 즉흥 멜로디 (색소폰)
    sax = pretty_midi.Instrument(program=65)
    start_time = 0
    for note in generated_melody:
        midi_note = pretty_midi.Note(velocity=110, pitch=note, start=start_time, end=start_time + 0.5)
        sax.notes.append(midi_note)
        start_time += 0.5
    midi.instruments.append(sax)

    # 🥁 드럼 트랙 수정 (스윙 리듬 반영)
    drums = pretty_midi.Instrument(program=0, is_drum=True)

    start_time = 0
    for i in range(output_length):
        # 🎶 하이햇 (스윙 리듬) - 8분음표 스윙 (offbeat 포함)
        if i % 2 == 0:
            hihat = pretty_midi.Note(velocity=80, pitch=42, start=start_time, end=start_time + 0.1)
            drums.notes.append(hihat)
        if i % 4 == 1:
            hihat_offbeat = pretty_midi.Note(velocity=75, pitch=42, start=start_time + 0.75, end=start_time + 0.85)
            drums.notes.append(hihat_offbeat)

        # 🥁 스네어 드럼 - 2박, 4박 강조
        if i % 4 == 2:
            snare = pretty_midi.Note(velocity=100, pitch=38, start=start_time, end=start_time + 0.1)
            drums.notes.append(snare)

        # 🥁 킥 드럼 - 1박, 3박 강조
        if i % 4 == 0:
            kick = pretty_midi.Note(velocity=110, pitch=36, start=start_time, end=start_time + 0.1)
            drums.notes.append(kick)

        start_time += 0.5

    # 🎵 드럼 트랙 추가
    midi.instruments.append(drums)

    # ✅ MIDI 파일 저장
    midi_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/midi/generated_jazz_enhanced.mid"
    midi.write(midi_path)
    print(f"🎶 재즈 MIDI 파일 저장 완료: {midi_path}")

# 📌 새로운 코드 진행 입력
user_chord_progression = ["Cmaj7", "Gmaj7", "FMinor", "DMinor", "Cmaj7", "Gmaj7", "Caug", "A7"]
generate_jazz_midi(model, user_chord_progression)