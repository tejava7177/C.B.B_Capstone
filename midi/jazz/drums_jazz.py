import pretty_midi
import random


def add_jazz_drum_track(midi, start_time, duration, chord_progression, swing_ratio=0.6):
    """🥁 재즈 드럼 트랙 추가 (스윙 리듬 적용)"""

    drum = pretty_midi.Instrument(program=0, is_drum=True)

    # 🎵 MIDI 드럼 음표 번호 (General MIDI Standard)
    kick_drum = 36  # Bass Drum
    snare_drum = 38  # Snare Drum
    ride_cymbal = 51  # Ride Cymbal (재즈 드럼의 핵심)
    hi_hat_closed = 42  # Closed Hi-Hat
    hi_hat_open = 46  # Open Hi-Hat
    brush_snare = 40  # 브러쉬 스네어 (부드러운 톤)

    for bar in range(len(chord_progression)):
        bar_start_time = start_time + (bar * duration)

        for i in range(8):  # 8비트 스윙 리듬 (Triplet Feel)
            beat_time = bar_start_time + (i * (duration / 8))

            # 🎵 스윙 리듬 적용 (뒤 박자를 살짝 밀기)
            if i % 2 == 1:
                beat_time += (duration / 8) * (swing_ratio - 0.5)

            # 🥁 라이드 심벌 (재즈의 기본 리듬)
            drum.notes.append(pretty_midi.Note(
                velocity=85, pitch=ride_cymbal, start=beat_time, end=beat_time + 0.1
            ))

            # 🥁 킥 드럼 (1, 3박 위주)
            if i % 4 == 0:
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(90, 110), pitch=kick_drum, start=beat_time, end=beat_time + 0.1
                ))

            # 🥁 스네어 드럼 (2, 4박 강조)
            if i % 4 == 2:
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(80, 100), pitch=snare_drum, start=beat_time, end=beat_time + 0.1
                ))

        # 🎵 심벌 변형 (4마디마다 크래시 추가)
        if bar % 4 == 3:
            crash_time = bar_start_time
            drum.notes.append(pretty_midi.Note(
                velocity=110, pitch=hi_hat_open, start=crash_time, end=crash_time + 0.3
            ))

    midi.instruments.append(drum)