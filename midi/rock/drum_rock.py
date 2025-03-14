import pretty_midi
import random

# 🎸 락 드럼 MIDI 프로그램 번호 (General MIDI 표준 Percussion 채널)
KICK = 36  # 킥 드럼
SNARE = 38  # 스네어 드럼
HIHAT_CLOSED = 42  # 클로즈 하이햇
HIHAT_OPEN = 46  # 오픈 하이햇
CRASH_CYMBAL = 49  # 크래시 심벌
RIDE_CYMBAL = 51  # 라이드 심벌
TOM1 = 48  # 하이 톰
TOM2 = 45  # 미들 톰
FLOOR_TOM = 43  # 플로어 톰

# 🎵 락 드럼 기본 패턴 (8비트 기반)
ROCK_DRUM_PATTERNS = [
    [KICK, None, SNARE, None, KICK, KICK, SNARE, None],  # 기본 패턴
    [KICK, SNARE, KICK, SNARE, KICK, KICK, SNARE, None],  # 변형 패턴
    [KICK, None, SNARE, KICK, KICK, None, SNARE, None],  # 더블 킥 포함 패턴
]

# 🎵 드럼 필인 (Fills)
ROCK_DRUM_FILLS = [
    [TOM1, TOM2, FLOOR_TOM, SNARE],  # 기본 톰 필인
    [KICK, TOM1, TOM2, FLOOR_TOM, CRASH_CYMBAL],  # 크래시 심벌 포함
    [TOM1, TOM1, TOM2, SNARE, CRASH_CYMBAL],  # 반복 톰 필인
]


def add_rock_drum_track(midi, start_time, duration, num_bars=8):
    """🎸 락 드럼 트랙 추가"""

    drum_track = pretty_midi.Instrument(program=0, is_drum=True)  # 🥁 드럼 트랙

    for bar in range(num_bars):
        bar_start_time = start_time + bar * duration
        drum_pattern = random.choice(ROCK_DRUM_PATTERNS)  # ✅ 랜덤 패턴 선택

        for i, note in enumerate(drum_pattern):
            if note:
                note_time = bar_start_time + (i * (duration / 8))  # 8비트 기준 배치
                velocity = random.randint(80, 110)  # 강약 조절

                drum_track.notes.append(pretty_midi.Note(
                    velocity=velocity,
                    pitch=note,
                    start=note_time,
                    end=note_time + 0.15  # 짧은 타격
                ))

        # 🔥 랜덤하게 필인 추가 (8마디마다 한 번)
        if bar % 4 == 3:
            fill_pattern = random.choice(ROCK_DRUM_FILLS)
            fill_time = bar_start_time + (7 * (duration / 8))  # 8박자 중 마지막 부분에 필인 추가

            for j, fill_note in enumerate(fill_pattern):
                drum_track.notes.append(pretty_midi.Note(
                    velocity=random.randint(90, 120),
                    pitch=fill_note,
                    start=fill_time + (j * 0.05),
                    end=fill_time + (j * 0.2)
                ))

    midi.instruments.append(drum_track)