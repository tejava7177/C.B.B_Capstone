import pretty_midi
import sys
import os

# ✅ `chord_to_notes.py`가 있는 경로 추가
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")

# ✅ CHORD_TO_NOTES 가져오기
from chord_to_notes import CHORD_TO_NOTES


def add_guitar_track(midi, chord_progression, start_time, duration):
    """ 기타 코드 진행을 MIDI에 추가 """
    guitar = pretty_midi.Instrument(program=25)  # Acoustic Guitar

    for chord in chord_progression:
        midi_notes = CHORD_TO_NOTES.get(chord, [60, 64, 67])  # 기본값: C Major
        midi_notes = [n - 12 for n in midi_notes]  # 기타는 1옥타브 낮게 연주
        for note_number in midi_notes:
            note = pretty_midi.Note(velocity=90, pitch=note_number, start=start_time, end=start_time + duration)
            guitar.notes.append(note)

        start_time += duration  # 다음 코드로 진행

    midi.instruments.append(guitar)