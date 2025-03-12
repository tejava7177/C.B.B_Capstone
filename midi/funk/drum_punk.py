import pretty_midi
import random

# 🥁 펑크 드럼 MIDI Program 설정 (General MIDI에서 드럼은 항상 0번)
DRUM_PROGRAM = 0

# 🥁 펑크 드럼 기본 요소 (MIDI Note 번호)
KICK = 36  # 베이스 드럼 (둥)
SNARE = 38  # 스네어 (탁)
HIHAT_CLOSED = 42  # 닫힌 하이햇 (츠츠)
HIHAT_OPEN = 46  # 열린 하이햇 (츠챠)
CRASH = 49  # 크래시 심벌 (쨍)

# 🥁 펑크 리듬 패턴 (8비트 기반)
PUNK_DRUM_PATTERNS = [
    [KICK, HIHAT_CLOSED, SNARE, HIHAT_CLOSED],  # 기본 8비트 패턴
    [KICK, HIHAT_CLOSED, SNARE, HIHAT_CLOSED, KICK, SNARE],  # 추가 킥
    [KICK, SNARE, KICK, SNARE, CRASH],  # 심벌 강조
]


def add_punk_drum_track(midi, start_time, duration, num_bars):
    """🥁 펑크 스타일 드럼 트랙 추가"""
    drum = pretty_midi.Instrument(program=DRUM_PROGRAM, is_drum=True)

    for bar in range(num_bars):
        bar_start_time = start_time + (bar * duration)

        # 랜덤한 패턴 선택
        pattern = random.choice(PUNK_DRUM_PATTERNS)

        for i, drum_note in enumerate(pattern):
            beat_time = bar_start_time + (i * (duration / len(pattern)))

            # 랜덤한 세기 적용
            velocity = random.randint(90, 120)

            drum.notes.append(pretty_midi.Note(
                velocity=velocity,
                pitch=drum_note,
                start=beat_time,
                end=beat_time + 0.1
            ))

    midi.instruments.append(drum)