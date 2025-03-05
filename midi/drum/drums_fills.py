import pretty_midi
from .drums_patterns import DRUM_NOTES

def add_fill(drum, start_time):
    """🥁 4마디마다 랜덤 필인 추가"""
    drum.notes.append(pretty_midi.Note(
        velocity=100, pitch=DRUM_NOTES["floor_tom"], start=start_time, end=start_time + 0.2
    ))
    drum.notes.append(pretty_midi.Note(
        velocity=100, pitch=DRUM_NOTES["tom2"], start=start_time + 0.2, end=start_time + 0.4
    ))
    drum.notes.append(pretty_midi.Note(
        velocity=110, pitch=DRUM_NOTES["tom1"], start=start_time + 0.4, end=start_time + 0.6
    ))
    drum.notes.append(pretty_midi.Note(
        velocity=120, pitch=DRUM_NOTES["crash"], start=start_time + 0.6, end=start_time + 0.8
    ))

    return drum

def add_cymbals(drum, start_time, bar):
    """🎵 크래시/라이드 심벌 추가"""
    if bar % 2 == 0:
        drum.notes.append(pretty_midi.Note(
            velocity=110, pitch=DRUM_NOTES["crash"], start=start_time, end=start_time + 0.2
        ))

    if bar % 4 == 2:
        drum.notes.append(pretty_midi.Note(
            velocity=90, pitch=DRUM_NOTES["ride"], start=start_time, end=start_time + 0.3
        ))

    return drum