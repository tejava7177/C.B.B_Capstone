import pretty_midi
import sys
import os

# 🛠️ `chord_to_notes.py`가 있는 폴더의 절대 경로 추가
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")

# ✅ 모듈 불러오기
from chord_to_notes import CHORD_TO_NOTES

def save_chord_progression_to_midi(chord_progression, bpm=120, filename="output.mid"):
    """AI가 생성한 코드 진행을 MIDI 파일로 변환 (4박자로 설정)"""

    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    start_time = 0.0
    beats_per_second = bpm / 60.0  # BPM을 초 단위로 변환
    chord_duration = 4 / beats_per_second  # 4박자 지속 시간

    for chord in chord_progression:
        midi_notes = CHORD_TO_NOTES.get(chord, [60, 64, 67])  # 코드 노트 변환

        for note_number in midi_notes:
            note = pretty_midi.Note(
                velocity=100, pitch=note_number, start=start_time, end=start_time + chord_duration
            )
            instrument.notes.append(note)

        start_time += chord_duration  # 다음 코드로 진행

    midi.instruments.append(instrument)
    midi.write(filename)
    print(f"✅ MIDI 파일이 생성되었습니다: {filename}")


# 🎵 AI가 생성한 코드 진행 (샘플)
ai_generated_chords = ["C9", "G9", "F9", "E7", "G9", "E Major", "G9", "Amaj7",
                       "Cmaj7", "Bsus4", "Dmaj7", "D9", "Amaj7", "Dmaj7", "B7"]

# MIDI 파일 생성 (4박자 적용)
save_chord_progression_to_midi(ai_generated_chords, bpm=120, filename="ai_generated_chords_4beats.mid")