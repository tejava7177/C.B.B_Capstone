import pretty_midi
import random


def add_jazz_drum_track(midi, start_time, duration, chord_progression, swing_ratio=0.6):
    """🥁 자연스러운 재즈 드럼 트랙 (랜덤 스윙 리듬 + 필인 추가)"""

    drum = pretty_midi.Instrument(program=0, is_drum=True)

    # 🎵 MIDI 드럼 음표 번호 (General MIDI Standard)
    kick_drum = 36  # Bass Drum
    snare_drum = 38  # Snare Drum
    ride_cymbal = 51  # Ride Cymbal (재즈 드럼의 핵심)
    hi_hat_closed = 42  # Closed Hi-Hat
    hi_hat_open = 46  # Open Hi-Hat
    brush_snare = 40  # Brush Snare (브러쉬 스네어)

    for bar in range(len(chord_progression)):
        bar_start_time = start_time + (bar * duration)

        for i in range(8):  # 🎵 8비트 스윙 리듬 (Triplet Feel)
            beat_time = bar_start_time + (i * (duration / 8))

            # ✅ 랜덤한 스윙 리듬 적용 (뒤 박자를 살짝 밀기)
            if i % 2 == 1:
                swing_offset = random.uniform(0.45, 0.65)  # 스윙 비율을 랜덤하게 조정
                beat_time += (duration / 8) * (swing_offset - 0.5)

            # ✅ 라이드 심벌 (스윙 리듬 패턴 변형)
            ride_velocity = random.randint(75, 90)
            drum.notes.append(pretty_midi.Note(
                velocity=ride_velocity, pitch=ride_cymbal, start=beat_time, end=beat_time + 0.1
            ))

            # ✅ 킥 드럼 (1, 3박 위주 + 랜덤 변형)
            if i % 4 == 0 or (random.random() > 0.85 and i % 2 == 0):  # 일부 변형
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(90, 110), pitch=kick_drum, start=beat_time, end=beat_time + 0.1
                ))

            # ✅ 스네어 드럼 (2, 4박 강조 + 랜덤 변형)
            if i % 4 == 2 or (random.random() > 0.7 and i % 4 == 3):
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(80, 100), pitch=snare_drum, start=beat_time, end=beat_time + 0.1
                ))

        # ✅ 랜덤한 브러쉬 드럼 패턴 추가 (일부 마디에서 변형)
        if random.random() > 0.6:
            brush_time = bar_start_time + (random.uniform(0.2, 0.8) * duration)
            drum.notes.append(pretty_midi.Note(
                velocity=random.randint(60, 90), pitch=brush_snare, start=brush_time, end=brush_time + 0.1
            ))

        # ✅ 4마디마다 필인(Fill-in) 추가 (랜덤한 필인 변형)
        if bar % 4 == 3:
            fill_time = bar_start_time + (7 * (duration / 8))  # 마지막 박자에 필인 추가
            drum.notes.append(pretty_midi.Note(
                velocity=100, pitch=snare_drum, start=fill_time, end=fill_time + 0.15
            ))
            drum.notes.append(pretty_midi.Note(
                velocity=110, pitch=brush_snare, start=fill_time + 0.15, end=fill_time + 0.3
            ))
            drum.notes.append(pretty_midi.Note(
                velocity=120, pitch=kick_drum, start=fill_time + 0.3, end=fill_time + 0.45
            ))
            drum.notes.append(pretty_midi.Note(
                velocity=120, pitch=ride_cymbal, start=fill_time + 0.45, end=fill_time + 0.6
            ))

        # ✅ 심벌 변형 (4마디마다 오픈 하이햇 추가)
        if bar % 4 == 2:
            crash_time = bar_start_time + (random.uniform(0.1, 0.3) * duration)
            drum.notes.append(pretty_midi.Note(
                velocity=110, pitch=hi_hat_open, start=crash_time, end=crash_time + 0.3
            ))

    midi.instruments.append(drum)