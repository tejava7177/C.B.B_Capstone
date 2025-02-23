import pretty_midi
import random

def add_drum_track(midi, start_time, duration, chord_progression):
    """ 드럼 패턴을 8비트 + 필인으로 개선 """

    drum = pretty_midi.Instrument(program=0, is_drum=True)

    kick_drum = 36
    snare_drum = 38
    closed_hihat = 42
    open_hihat = 46
    crash_cymbal = 49
    tom1 = 48
    tom2 = 45

    for bar in range(len(chord_progression)):
        bar_start_time = start_time + (bar * duration)

        for i in range(8):
            beat_time = bar_start_time + (i * (duration / 8))

            if i % 2 == 0:
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(90, 120), pitch=kick_drum, start=beat_time, end=beat_time + 0.1
                ))

        # 🎵 랜덤 필 추가
        if bar % 4 == 3:
            drum.notes.append(pretty_midi.Note(velocity=110, pitch=tom1, start=bar_start_time + 3.2, end=bar_start_time + 3.4))

    midi.instruments.append(drum)