import pretty_midi
import random
import sys
import os

# ✅ CHORD_TO_NOTES 가져오기
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES

def add_guitar_track(midi, chord_progression, start_time, duration):
    """🎸 일렉 기타 트랙 추가 (랜덤한 연주 스타일 적용)"""

    guitar = pretty_midi.Instrument(program=27)  # ✅ Electric Guitar (Clean)

    # ✅ 🎵 랜덤한 연주 스타일 선택
    play_style = random.choice(["strumming", "arpeggio", "power_chord"])

    for chord in chord_progression:
        # ✅ CHORD_TO_NOTES에서 코드 찾기 (없으면 C Major 기본 코드 사용)
        if chord in CHORD_TO_NOTES:
            midi_notes = CHORD_TO_NOTES[chord]
        else:
            print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 정의되지 않았음. 기본 코드 사용")
            midi_notes = CHORD_TO_NOTES.get("C Major", [60, 64, 67])

        # ✅ 숫자로 변환 후 1옥타브 낮춤
        midi_notes = [int(n) - 12 for n in midi_notes]

        # ✅ 🎸 코드 연주 방식에 따른 패턴 적용
        if play_style == "strumming":
            # 🎵 다운스트로크 + 업스트로크 조합
            for i, note_number in enumerate(midi_notes):
                note_start = start_time + (i * 0.15)
                note_end = note_start + (duration * 0.4)
                velocity = random.randint(80, 110)

                guitar.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_number, start=note_start, end=note_end
                ))

        elif play_style == "arpeggio":
            # 🎵 한 음씩 아르페지오 스타일로 연주
            for i, note_number in enumerate(midi_notes):
                note_start = start_time + (i * 0.2)
                note_end = note_start + (duration * 0.5)
                velocity = random.randint(90, 110)

                guitar.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_number, start=note_start, end=note_end
                ))

        elif play_style == "power_chord":
            # 🎵 파워 코드 (루트 + 5도만 연주)
            power_chord_notes = [midi_notes[0], midi_notes[0] + 7]
            for note_number in power_chord_notes:
                note_start = start_time
                note_end = note_start + (duration * 0.7)
                velocity = random.randint(100, 120)

                guitar.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_number, start=note_start, end=note_end
                ))

        # 🎸 코드 기반 리드 멜로디 추가 (랜덤 솔로 느낌)
        melody_note = random.choice(midi_notes + [midi_notes[0] + 5, midi_notes[1] + 7, midi_notes[2] + 12])
        melody_start = start_time + random.uniform(0.5, 1.5)
        melody_end = melody_start + random.uniform(0.3, 0.6)
        velocity = random.randint(100, 120)

        guitar.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=melody_note, start=melody_start, end=melody_end
        ))

        start_time += duration

    midi.instruments.append(guitar)