import pretty_midi
import random

def add_drum_track(midi, start_time, duration, chord_progression):
    """ 코드 진행 전체(15코드) 동안 4박자를 꽉 채운 드럼 패턴 추가 """

    drum = pretty_midi.Instrument(program=0, is_drum=True)

    # 🎵 드럼 음표 정의 (General MIDI Percussion)
    kick_drum = 36  # Bass Drum
    snare_drum = 38  # Snare Drum
    closed_hihat = 42
    open_hihat = 46
    crash_cymbal = 49
    ride_cymbal = 51
    tom1 = 48  # High Tom
    tom2 = 45  # Low Tom

    # 🎯 코드 진행 전체 길이 (15코드 = 15마디)
    total_bars = len(chord_progression)  # 코드 개수만큼 드럼을 반복

    # 🔥 코드 진행 전체 동안 반복되는 4박자 드럼 패턴
    for bar in range(total_bars):
        bar_start_time = start_time + (bar * duration)  # 코드 진행 시간에 맞춰 드럼 반복

        for i in range(4):  # 4박자 루프
            beat_time = bar_start_time + (i * (duration / 4))

            # 🎯 킥 드럼 (1박 & 3박)
            if i % 2 == 0:
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(90, 120), pitch=kick_drum, start=beat_time, end=beat_time + 0.1
                ))

            # 🎯 스네어 드럼 (2박 & 4박)
            if i % 2 == 1:
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(90, 120), pitch=snare_drum, start=beat_time, end=beat_time + 0.1
                ))

            # 🎯 하이햇 (Closed & Open 랜덤 섞기)
            if random.random() > 0.7:
                drum.notes.append(pretty_midi.Note(
                    velocity=80, pitch=open_hihat, start=beat_time, end=beat_time + 0.1
                ))
            else:
                drum.notes.append(pretty_midi.Note(
                    velocity=80, pitch=closed_hihat, start=beat_time, end=beat_time + 0.1
                ))

        # 🎵 8마디마다 심벌 크래시 & 탐탐 필 추가
        if (bar % 8) == 0:
            drum.notes.append(pretty_midi.Note(
                velocity=100, pitch=crash_cymbal, start=bar_start_time, end=bar_start_time + 0.5
            ))
            drum.notes.append(pretty_midi.Note(
                velocity=90, pitch=tom1, start=bar_start_time + 0.6, end=bar_start_time + 0.7
            ))
            drum.notes.append(pretty_midi.Note(
                velocity=90, pitch=tom2, start=bar_start_time + 0.7, end=bar_start_time + 0.8
            ))

    midi.instruments.append(drum)