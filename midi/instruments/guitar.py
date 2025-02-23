import pretty_midi
import sys
import os
import random

# ✅ CHORD_TO_NOTES 가져오기
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES

def add_guitar_track(midi, chord_progression, start_time, duration):
    """ 일렉 기타 리프(Lead Line) 추가 """

    guitar = pretty_midi.Instrument(program=29)  # Overdrive Guitar

    for chord in chord_progression:
        if chord in CHORD_TO_NOTES:
            midi_notes = CHORD_TO_NOTES[chord]
        else:
            print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 정의되지 않았음. 기본 코드 사용")
            midi_notes = CHORD_TO_NOTES.get("C Major", [60, 64, 67])

        midi_notes = [int(n) for n in midi_notes]
        midi_notes = [n - 12 for n in midi_notes]  # 기타 음역으로 변환

        # 🎸 기본 코드 톤 연주 (다운스트로크)
        for i, note_number in enumerate(midi_notes):
            note_start = start_time + (i * 0.2)
            note_end = note_start + (duration * 0.5)
            velocity = random.randint(90, 110)

            guitar.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=note_number, start=note_start, end=note_end
            ))

        # 🎸 코드 기반 멜로디 추가 (루트음 + 3도 + 랜덤 5도 or 7도)
        melody_note = random.choice(midi_notes + [midi_notes[0] + 5, midi_notes[1] + 7])
        guitar.notes.append(pretty_midi.Note(
            velocity=100, pitch=melody_note, start=start_time + 1.2, end=start_time + 1.8
        ))

        start_time += duration

    midi.instruments.append(guitar)