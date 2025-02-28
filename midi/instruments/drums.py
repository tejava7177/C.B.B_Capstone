import pretty_midi
import random

def add_drum_track(midi, start_time, duration, chord_progression, bpm=120):
    """🥁 더 자연스러운 드럼 패턴 (랜덤 리듬 스타일 적용 + 필인 변형)"""

    drum = pretty_midi.Instrument(program=0, is_drum=True)

    # 🎵 MIDI 드럼 음표 번호 (General MIDI Standard)
    kick_drum = 36  # Bass Drum
    snare_drum = 38  # Snare Drum
    closed_hihat = 42  # Hi-Hat 닫힘
    open_hihat = 46  # Hi-Hat 열림
    ride_cymbal = 51  # Ride Cymbal
    crash_cymbal = 49  # Crash Cymbal
    tom1 = 48  # High Tom
    tom2 = 47  # Mid Tom
    floor_tom = 45  # Floor Tom

    # ✅ 🎵 "틱 틱 틱 틱" Click Track 도입부 (하이햇 닫힘)
    click_duration = 60 / bpm  # 한 박자의 길이
    click_start_time = start_time
    for i in range(4):  # 4박자 Click Track
        tick_time = click_start_time + (i * click_duration)
        drum.notes.append(pretty_midi.Note(
            velocity=100, pitch=closed_hihat, start=tick_time, end=tick_time + 0.1
        ))

    # ✅ 기존 드럼 시작 시간 조정 (Click Track 이후)
    start_time += 4 * click_duration  # "틱 틱 틱 틱" 도입부 이후 악기 시작

    # 🎵 랜덤한 드럼 패턴 스타일 선택
    rhythm_pattern = random.choice(["straight_8beat", "shuffle", "funky"])

    for bar in range(len(chord_progression)):
        bar_start_time = start_time + (bar * duration)

        for i in range(8):  # 8비트 기본 박자
            beat_time = bar_start_time + (i * (duration / 8))

            # 🥁 베이스 드럼 패턴 (스타일에 따라 변화)
            if rhythm_pattern == "straight_8beat":
                if i % 4 == 0 or (random.random() > 0.7 and i % 2 == 0):
                    drum.notes.append(pretty_midi.Note(
                        velocity=random.randint(90, 110), pitch=kick_drum, start=beat_time, end=beat_time + 0.1
                    ))

            elif rhythm_pattern == "shuffle":
                if i % 3 == 0:
                    drum.notes.append(pretty_midi.Note(
                        velocity=random.randint(90, 110), pitch=kick_drum, start=beat_time, end=beat_time + 0.1
                    ))

            elif rhythm_pattern == "funky":
                if i % 4 == 0 or (random.random() > 0.5 and i % 2 == 0):
                    drum.notes.append(pretty_midi.Note(
                        velocity=random.randint(90, 110), pitch=kick_drum, start=beat_time, end=beat_time + 0.1
                    ))

            # 🥁 스네어 드럼 (기본 2, 4박자 + 랜덤 변형)
            if i % 4 == 2 or (random.random() > 0.8 and i % 4 == 3):
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(80, 100), pitch=snare_drum, start=beat_time, end=beat_time + 0.1
                ))

            # 🎵 하이햇 패턴 (스타일별 변형)
            if rhythm_pattern == "straight_8beat":
                if random.random() > 0.7:
                    drum.notes.append(pretty_midi.Note(
                        velocity=80, pitch=open_hihat, start=beat_time, end=beat_time + 0.1
                    ))
                else:
                    drum.notes.append(pretty_midi.Note(
                        velocity=80, pitch=closed_hihat, start=beat_time, end=beat_time + 0.1
                    ))

            elif rhythm_pattern == "shuffle":
                if i % 3 != 0:  # Shuffle 특유의 하이햇 패턴
                    drum.notes.append(pretty_midi.Note(
                        velocity=80, pitch=closed_hihat, start=beat_time, end=beat_time + 0.1
                    ))

            elif rhythm_pattern == "funky":
                if i % 4 == 1 or i % 4 == 3:  # 펑키한 하이햇 패턴
                    drum.notes.append(pretty_midi.Note(
                        velocity=90, pitch=open_hihat, start=beat_time, end=beat_time + 0.1
                    ))
                else:
                    drum.notes.append(pretty_midi.Note(
                        velocity=80, pitch=closed_hihat, start=beat_time, end=beat_time + 0.1
                    ))

        # 🎸 드럼 필인 (4마디마다 랜덤 필인)
        if bar % 4 == 3:
            fill_time = bar_start_time + (7 * (duration / 8))  # 마지막 박자에 필인 추가
            drum.notes.append(pretty_midi.Note(
                velocity=100, pitch=floor_tom, start=fill_time, end=fill_time + 0.2
            ))
            drum.notes.append(pretty_midi.Note(
                velocity=100, pitch=tom2, start=fill_time + 0.2, end=fill_time + 0.4
            ))
            drum.notes.append(pretty_midi.Note(
                velocity=110, pitch=tom1, start=fill_time + 0.4, end=fill_time + 0.6
            ))
            drum.notes.append(pretty_midi.Note(
                velocity=120, pitch=crash_cymbal, start=fill_time + 0.6, end=fill_time + 0.8
            ))

        # 🎵 크래시 심벌 추가 (코드 변경 시 강조)
        if bar % 2 == 0:
            crash_time = bar_start_time
            drum.notes.append(pretty_midi.Note(
                velocity=110, pitch=crash_cymbal, start=crash_time, end=crash_time + 0.2
            ))

        # 🎵 라이드 심벌 추가 (후반부 다이내믹 조절)
        if bar % 4 == 2:
            ride_time = bar_start_time
            drum.notes.append(pretty_midi.Note(
                velocity=90, pitch=ride_cymbal, start=ride_time, end=ride_time + 0.3
            ))

    midi.instruments.append(drum)