import pretty_midi
import random

# ✅ 상대 경로로 변경 (현재 폴더 기준)
from drum.drums_patterns import apply_rhythm_pattern
from drum.drums_fills import add_fill, add_cymbals
from drum.drums_utils import select_random_pattern

def add_drum_track(midi, start_time, duration, chord_progression):
    """🥁 드럼 트랙 생성"""
    drum = pretty_midi.Instrument(program=0, is_drum=True)
    rhythm_pattern = select_random_pattern()

    for bar in range(len(chord_progression)):
        bar_start_time = start_time + (bar * duration)

        # 🎵 리듬 패턴 적용
        drum = apply_rhythm_pattern(drum, bar_start_time, duration, rhythm_pattern)

        # 🎵 필인 및 심벌 추가
        if bar % 4 == 3:
            drum = add_fill(drum, bar_start_time + (7 * (duration / 8)))
        drum = add_cymbals(drum, bar_start_time, bar)

    midi.instruments.append(drum)