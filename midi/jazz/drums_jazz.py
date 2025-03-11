import pretty_midi
import random

def add_jazz_drum_track(midi, start_time, duration, chord_progression):
    """🥁 재즈 드럼 트랙 추가 (3/4 박자 & 스윙 리듬 적용)"""

    drum = pretty_midi.Instrument(program=0, is_drum=True)

    # 🎵 MIDI 드럼 음표 번호 (General MIDI Standard)
    kick_drum = 36  # Bass Drum
    snare_drum = 38  # Snare Drum
    ride_cymbal = 51  # Ride Cymbal (재즈 드럼의 핵심)

    for bar in range(len(chord_progression)):
        bar_start_time = start_time + (bar * duration)

        for i in range(3):  # 🎵 3/4 박자 패턴
            beat_time = bar_start_time + (i * (duration / 3))

            # 🥁 라이드 심벌 (3/4 스윙 리듬: 칭-치-치-칭)
            ride_velocity = 80 if i == 0 else 60  # 🎵 강약 조절 (첫 박 강하게)
            drum.notes.append(pretty_midi.Note(
                velocity=ride_velocity, pitch=ride_cymbal, start=beat_time, end=beat_time + 0.1
            ))

            # 🥁 킥 드럼 (1박 위주)
            if i == 0:
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(90, 110), pitch=kick_drum, start=beat_time, end=beat_time + 0.1
                ))

            # 🥁 스네어 드럼 (2박 강조)
            if i == 1:
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(80, 100), pitch=snare_drum, start=beat_time, end=beat_time + 0.1
                ))

    midi.instruments.append(drum)