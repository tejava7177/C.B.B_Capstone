import pretty_midi
import random
import sys

# ✅ CHORD_TO_NOTES 가져오기 (chord_map.py 활용)
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES

# 🎹 예외 처리를 위한 기본 재즈 코드 보이싱
JAZZ_VOICINGS = {
    "Cmaj7": [60, 64, 67, 71],
    "Dm7": [62, 65, 69, 72],
    "G7": [43, 50, 53, 57],
    "Fmaj7": [41, 45, 48, 52],
    "Bm7": [47, 50, 54, 57],
    "E7": [40, 47, 50, 54],
    "Am7": [45, 48, 52, 55]
}

# 🎵 느린 박자 리듬 패턴
SLOW_RHYTHM_PATTERNS = [
    [0],  # 첫 박자에서 코드 연주 후 유지
    [0, 2],  # 첫 박자와 셋째 박자에서 연주
    [0, 3],  # 첫 박자와 넷째 박자에서 연주
]

# 🎵 싱글노트 멜로디 패턴 (필인용)
SINGLE_NOTE_PATTERNS = [
    [1.5],  # 2박 반에서 싱글 노트
    [2.5],  # 3박 반에서 싱글 노트
    [1, 2.5],  # 2박, 3박 반에서 싱글 노트
]


def get_piano_chord_variation(chord):
    """🎵 코드에 따른 재즈 보이싱 생성 (CHORD_TO_NOTES 활용)"""

    # 🎯 리스트가 들어왔을 경우 첫 번째 값 사용
    if isinstance(chord, list):
        chord = chord[0]  # ✅ 리스트의 첫 번째 코드만 사용

    # 🎯 숫자(MIDI 노트 값)가 들어왔다면 변환하지 않음
    if isinstance(chord, (int, float)):
        print(f"⚠️ Warning: MIDI Note '{chord}'가 코드로 감지됨. 변환하지 않음.")
        return [chord]

    # 🎯 코드가 CHORD_TO_NOTES에 있는지 확인
    if chord in CHORD_TO_NOTES:
        base_notes = CHORD_TO_NOTES[chord]
    else:
        print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 없음. 기본 C Major 사용")
        base_notes = CHORD_TO_NOTES["C Major"]  # ✅ Cmaj7 대신 C Major 사용

    return base_notes[:4]  # 4개 음만 사용
def add_jazz_piano_track(midi, start_time, duration, chord_progression):
    """🎹 재즈 피아노 코드 컴핑 (느린 박자, 부드러운 연결)"""

    piano = pretty_midi.Instrument(program=0)  # 🎹 Acoustic Grand Piano

    for bar, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar * duration)
        chord_notes = get_piano_chord_variation(chord)  # ✅ CHORD_TO_NOTES 기반으로 코드 보이싱 생성

        # ✅ 랜덤한 느린 리듬 패턴 선택
        rhythm_pattern = random.choice(SLOW_RHYTHM_PATTERNS)

        # ✅ 왼손 (저음 루트음)과 오른손 (보이싱)을 분리
        left_hand = [chord_notes[0] - 12]  # 루트 노트 (옥타브 낮춤)
        right_hand = chord_notes[1:]  # 나머지 보이싱

        for beat in rhythm_pattern:
            beat_time = bar_start_time + (beat * (duration / 4))
            beat_time += random.uniform(-0.05, 0.05)  # 🎵 박자 랜덤 딜레이

            # 🎹 왼손 (루트음) 추가 - 길게 유지
            for note in left_hand:
                piano.notes.append(pretty_midi.Note(
                    velocity=random.randint(70, 90),
                    pitch=note,
                    start=beat_time,
                    end=beat_time + duration * random.uniform(0.7, 1.0)  # 랜덤한 길이
                ))

            # 🎹 오른손 (코드 보이싱) 추가 - 부드러운 시간차 적용
            for i, note in enumerate(right_hand):
                delay = random.uniform(0.05, 0.15) * i  # 🎵 부드러운 연결감 (시간차 적용)
                note_length = duration * random.uniform(0.5, 0.8)  # 🎵 랜덤한 길이 적용
                piano.notes.append(pretty_midi.Note(
                    velocity=random.randint(75, 95),
                    pitch=note,
                    start=beat_time + delay,
                    end=beat_time + note_length
                ))

    midi.instruments.append(piano)