import pretty_midi
import sys
import os
import random

# ✅ CHORD_TO_NOTES 가져오기
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES


def add_piano_track(midi, chord_progression, start_time, duration):
    """ 피아노 코드 진행을 자연스럽게 변형 (아르페지오 + 코드 멜로디 추가) """

    piano = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    for chord in chord_progression:
        if chord in CHORD_TO_NOTES:
            midi_notes = CHORD_TO_NOTES[chord]
        else:
            print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 정의되지 않았음. 기본 코드 사용")
            midi_notes = CHORD_TO_NOTES.get("C Major", [60, 64, 67])

        midi_notes = [int(n) for n in midi_notes]  # 🎯 `int` 변환 추가

        # 🎹 코드톤을 활용하여 아르페지오 연주
        for i in range(4):
            for j, note_number in enumerate(midi_notes):
                velocity = 90 - (j * 10)  # 코드 구성음마다 강약 조절
                note_start = start_time + (i * (duration / 4)) + (j * 0.1)  # 각 음을 시간차로 연주
                note_end = note_start + (duration / 4)

                piano.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_number, start=note_start, end=note_end
                ))

        # 🎹 코드 진행에 멜로디 추가 (랜덤하게 7도나 9도 음을 삽입)
        melody_note = random.choice(midi_notes + [midi_notes[0] + 12, midi_notes[1] + 12])  # 옥타브 위 멜로디 추가
        piano.notes.append(pretty_midi.Note(
            velocity=100, pitch=melody_note, start=start_time + 1.5, end=start_time + 2.0
        ))

        start_time += duration  # 다음 코드로 진행

    midi.instruments.append(piano)