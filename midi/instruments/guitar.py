import pretty_midi
import random
import sys
import os

# ✅ CHORD_TO_NOTES 가져오기
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES


def add_guitar_backing_track(midi, chord_progression, start_time, duration):
    """🎸 기타 백킹 트랙 추가 (자연스러운 연주 느낌 반영)"""

    guitar = pretty_midi.Instrument(program=25)  # ✅ Acoustic Guitar (Steel)

    for chord in chord_progression:
        # ✅ CHORD_TO_NOTES에서 코드 찾기 (없으면 C Major 기본 코드 사용)
        if chord in CHORD_TO_NOTES:
            midi_notes = CHORD_TO_NOTES[chord]
        else:
            print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 정의되지 않았음. 기본 코드 사용")
            midi_notes = CHORD_TO_NOTES.get("C Major", [60, 64, 67])

        # ✅ 개방현 느낌을 추가하기 위해 1~2옥타브 낮추기
        midi_notes = [int(n) - random.choice([12, 24]) for n in midi_notes]

        # ✅ 리듬 패턴 적용
        rhythm_pattern = get_strumming_pattern("folk")  # 🎵 기본적으로 포크 스타일 스트럼 적용

        for i, stroke in enumerate(rhythm_pattern):
            if stroke == "-":  # 쉼표 처리
                continue

            note_start = start_time + (i * (duration / len(rhythm_pattern)))
            note_end = note_start + random.uniform(0.2, 0.3)  # 코드 지속 시간 랜덤화
            velocity = 100 if stroke == "down" else 80  # 다운스트로크는 강하게, 업스트로크는 약하게

            for note_number in midi_notes:
                guitar.notes.append(pretty_midi.Note(
                    velocity=velocity, pitch=note_number, start=note_start, end=note_end
                ))

        start_time += duration

    midi.instruments.append(guitar)


def get_strumming_pattern(genre="rock"):
    """🎵 장르별 기타 스트럼 패턴 반환"""
    patterns = {
        "pop": ["down", "down", "up", "down", "-", "up", "down", "up"],
        "rock": ["down", "-", "down", "down", "-", "down", "down", "-"],
        "folk": ["down", "up", "down", "-", "down", "up", "down", "up"]
    }
    return patterns.get(genre, patterns["folk"])  # 기본값: 포크 스타일