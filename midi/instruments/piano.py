import pretty_midi
import sys
import os
import random

# ✅ CHORD_TO_NOTES 가져오기
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES

def add_piano_track(midi, chord_progression, start_time, duration):
    """ 🎹 피아노 코드 진행을 자연스럽게 변형 (랜덤 리듬 패턴 + 코드 멜로디 추가) """

    piano = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    for chord in chord_progression:
        if chord in CHORD_TO_NOTES:
            midi_notes = CHORD_TO_NOTES[chord]
        else:
            print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 정의되지 않았음. 기본 코드 사용")
            midi_notes = CHORD_TO_NOTES.get("C Major", [60, 64, 67])

        midi_notes = [int(n) for n in midi_notes]  # 🎯 `int` 변환 추가

        # 🎵 랜덤 연주 스타일 선택
        rhythm_pattern = random.choice(["arpeggio", "block", "syncopation"])

        if rhythm_pattern == "arpeggio":
            # 🎹 코드톤을 활용하여 아르페지오 연주
            for i in range(4):  # 4박자 동안 연주
                for j, note_number in enumerate(midi_notes):
                    velocity = random.randint(70, 100)  # 🎵 강약 조절
                    note_start = start_time + (i * (duration / 4)) + (j * 0.1)  # 시간차 적용
                    note_end = note_start + (duration / 4)

                    piano.notes.append(pretty_midi.Note(
                        velocity=velocity, pitch=note_number, start=note_start, end=note_end
                    ))

        elif rhythm_pattern == "block":
            # 🎹 블록 코드 (같이 눌러서 연주)
            note_start = start_time
            note_end = note_start + duration
            velocity = random.randint(90, 110)  # 🎵 강한 블록 코드
            for note_number in midi_notes:
                piano.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_number, start=note_start, end=note_end
                ))

        elif rhythm_pattern == "syncopation":
            # 🎹 싱코페이션 리듬 적용
            syncopation_points = [0, 0.25, 0.5, 0.75, 1.0]
            for sync in syncopation_points:
                note_start = start_time + (sync * duration)
                note_end = note_start + (duration / 4)
                velocity = random.randint(75, 95)  # 약간 부드러운 연주

                piano.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=random.choice(midi_notes), start=note_start, end=note_end
                ))

        # 🎵 코드 진행에 멜로디 추가 (랜덤 옥타브 변경)
        melody_options = [midi_notes[0] + 12, midi_notes[1] + 12, midi_notes[2] + 12, midi_notes[0] + 7, midi_notes[1] + 9]
        melody_note = random.choice(melody_options)  # 랜덤 멜로디 선택
        melody_velocity = random.randint(80, 110)

        piano.notes.append(pretty_midi.Note(
            velocity=melody_velocity, pitch=melody_note, start=start_time + random.uniform(1.0, 2.5), end=start_time + 3.0
        ))

        start_time += duration  # 다음 코드로 진행

    midi.instruments.append(piano)