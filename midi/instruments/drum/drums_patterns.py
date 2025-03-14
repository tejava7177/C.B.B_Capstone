import pretty_midi
import random

# 🎵 MIDI 드럼 음표 번호
DRUM_NOTES = {
    "kick": 36,
    "snare": 38,
    "closed_hihat": 42,
    "open_hihat": 46,
    "ride": 51,
    "crash": 49,
    "tom1": 48,
    "tom2": 47,
    "floor_tom": 45,
}

def apply_rhythm_pattern(drum, start_time, duration, rhythm_pattern):
    """🥁 리듬 스타일 적용"""
    for i in range(8):  # 8비트 박자
        beat_time = start_time + (i * (duration / 8))

        # 베이스 드럼
        if rhythm_pattern == "straight_8beat":
            if i % 4 == 0 or (random.random() > 0.7 and i % 2 == 0):
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(90, 110), pitch=DRUM_NOTES["kick"], start=beat_time, end=beat_time + 0.1
                ))
        elif rhythm_pattern == "shuffle":
            if i % 3 == 0:
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(90, 110), pitch=DRUM_NOTES["kick"], start=beat_time, end=beat_time + 0.1
                ))
        elif rhythm_pattern == "funky":
            if i % 4 == 0 or (random.random() > 0.5 and i % 2 == 0):
                drum.notes.append(pretty_midi.Note(
                    velocity=random.randint(90, 110), pitch=DRUM_NOTES["kick"], start=beat_time, end=beat_time + 0.1
                ))

        # 스네어 드럼 (2, 4박자 기본)
        if i % 4 == 2 or (random.random() > 0.8 and i % 4 == 3):
            drum.notes.append(pretty_midi.Note(
                velocity=random.randint(80, 100), pitch=DRUM_NOTES["snare"], start=beat_time, end=beat_time + 0.1
            ))

        # 하이햇 패턴
        hihat_pitch = DRUM_NOTES["closed_hihat"] if random.random() > 0.7 else DRUM_NOTES["open_hihat"]
        drum.notes.append(pretty_midi.Note(
            velocity=80, pitch=hihat_pitch, start=beat_time, end=beat_time + 0.1
        ))

    return drum