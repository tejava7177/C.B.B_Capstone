import pretty_midi
import random

# 🥁 Punk 드럼 MIDI 프로그램 번호
DRUM_PROGRAM = 0  # MIDI Percussion Track

# 🥁 Punk 드럼 패턴
PUNK_DRUM_PATTERNS = {
    "kick": [0, 1, 2, 3],  # 4/4 기준, 모든 박자에서 킥 드럼
    "snare": [1, 3],  # 2, 4 박자에서 스네어 드럼
    "hihat": [0, 1, 2, 3],  # 모든 박자에서 하이햇
}

# 🥁 MIDI 드럼 노트 (General MIDI Percussion Key)
DRUM_NOTES = {
    "kick": 36,    # Bass Drum (둥)
    "snare": 38,   # Snare Drum (탁)
    "hihat": 42,   # Closed Hi-hat (츠)
    "crash": 49,   # Crash Cymbal
    "ride": 51     # Ride Cymbal
}

def add_punk_drum_track(midi, start_time, duration, num_bars):
    """🥁 Punk 드럼 트랙 생성"""

    drum_track = pretty_midi.Instrument(program=DRUM_PROGRAM, is_drum=True)

    for bar in range(num_bars):
        bar_start_time = start_time + (bar * duration)

        for beat in range(4):  # 4/4 박자 기준
            beat_time = bar_start_time + (beat * (duration / 4))

            # 🥁 Kick Drum (모든 박자)
            if beat in PUNK_DRUM_PATTERNS["kick"]:
                drum_track.notes.append(pretty_midi.Note(
                    velocity=random.randint(90, 110),
                    pitch=DRUM_NOTES["kick"],
                    start=beat_time,
                    end=beat_time + 0.1
                ))

            # 🥁 Snare Drum (2, 4박자 강한 스트로크)
            if beat in PUNK_DRUM_PATTERNS["snare"]:
                drum_track.notes.append(pretty_midi.Note(
                    velocity=random.randint(100, 120),
                    pitch=DRUM_NOTES["snare"],
                    start=beat_time,
                    end=beat_time + 0.1
                ))

            # 🥁 Hi-hat (전체 박자)
            if beat in PUNK_DRUM_PATTERNS["hihat"]:
                drum_track.notes.append(pretty_midi.Note(
                    velocity=random.randint(80, 100),
                    pitch=DRUM_NOTES["hihat"],
                    start=beat_time,
                    end=beat_time + 0.1
                ))

        # 🥁 Crash Cymbal (마디 첫 박자)
        drum_track.notes.append(pretty_midi.Note(
            velocity=random.randint(110, 127),
            pitch=DRUM_NOTES["crash"],
            start=bar_start_time,
            end=bar_start_time + 0.3
        ))

    midi.instruments.append(drum_track)