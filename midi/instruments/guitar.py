import pretty_midi
import random
import sys
import os

# ✅ CHORD_TO_NOTES 가져오기
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES

def add_guitar_lead_track(midi, chord_progression, start_time, duration):
    """🎸 기타 리드 트랙 추가 (코드 시작 부분 강조 + 멜로디)"""

    guitar = pretty_midi.Instrument(program=25)  # ✅ Distortion Guitar (Lead 역할)

    for chord in chord_progression:
        # ✅ CHORD_TO_NOTES에서 코드 찾기 (없으면 C Major 기본 코드 사용)
        if chord in CHORD_TO_NOTES:
            midi_notes = CHORD_TO_NOTES[chord]
        else:
            print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 정의되지 않았음. 기본 코드 사용")
            midi_notes = CHORD_TO_NOTES.get("C Major", [60, 64, 67])

        # ✅ 숫자로 변환 후 1옥타브 낮춤
        midi_notes = [int(n) - 12 for n in midi_notes]

        # 🎸 코드 시작 시 "루트음 + 5도"만 짧게 연주 (코드를 강조하는 역할)
        root_and_fifth = [midi_notes[0], midi_notes[0] + 7]
        for note_number in root_and_fifth:
            note_start = start_time
            note_end = note_start + (duration * 0.3)  # 짧게 코드 강조
            velocity = random.randint(100, 120)

            guitar.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=note_number, start=note_start, end=note_end
            ))

        # # 🎸 코드 진행 기반 리드 멜로디 (랜덤 패턴 추가)
        # melody_note = random.choice(midi_notes + [midi_notes[0] + 5, midi_notes[1] + 7, midi_notes[2] + 12])
        # melody_start = start_time + random.uniform(0.5, 1.5)
        # melody_end = melody_start + random.uniform(0.3, 0.6)
        # velocity = random.randint(100, 120)
        #
        # guitar.notes.append(pretty_midi.Note(
        #     velocity=velocity, pitch=melody_note, start=melody_start, end=melody_end
        # ))

        start_time += duration

    midi.instruments.append(guitar)