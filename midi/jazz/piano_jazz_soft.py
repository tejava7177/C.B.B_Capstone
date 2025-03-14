import pretty_midi
import random
import sys

# ✅ CHORD_TO_NOTES 가져오기
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

# 🎵 코드 지속 시간 (랜덤 적용)
CHORD_DURATIONS = [0.7, 0.85, 1.0, 1.2]  # 🎵 코드 길이를 다양하게 설정

def get_jazz_voicing(chord):
    """🎵 코드에 따른 재즈 보이싱 생성"""
    if chord in CHORD_TO_NOTES:
        return CHORD_TO_NOTES[chord]  # CHORD_TO_NOTES 활용
    return JAZZ_VOICINGS.get(chord, JAZZ_VOICINGS["Cmaj7"])  # 기본 Cmaj7

def add_jazz_piano_comping(midi, start_time, duration, chord_progression):
    """🎹 재즈 코드 컴핑 (첫 박자는 정박, 이후 부드러운 연결)"""

    piano = pretty_midi.Instrument(program=0)  # 🎹 Acoustic Grand Piano

    for bar, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar * duration)
        chord_notes = get_jazz_voicing(chord)  # ✅ 코드 변환 적용

        # ✅ 첫 박자는 **정확한 박자**에 맞춰 연주 (드럼과 타이트하게 맞춤)
        chord_start_time = bar_start_time  # ⏳ 첫 박자는 항상 정박

        # ✅ 코드 지속 시간 랜덤 설정 (다양한 길이 유지)
        chord_length = duration * random.choice(CHORD_DURATIONS)

        # 🎹 코드 컴핑 (부드러운 스트럼 효과)
        for i, note in enumerate(chord_notes):
            piano.notes.append(pretty_midi.Note(
                velocity=random.randint(70, 90),
                pitch=note,
                start=chord_start_time + (i * 0.02),  # 🎵 스트럼 효과 (부드러운 코드 연주)
                end=chord_start_time + chord_length
            ))

    midi.instruments.append(piano)