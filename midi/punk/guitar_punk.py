import pretty_midi
import random
import sys

# ✅ CHORD_TO_NOTES 가져오기 (Jazz에서 사용한 방식)
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES


# 🎸 Punk 기타 MIDI 프로그램 번호
GUITAR_PROGRAM = 30  # Distorted Guitar

# 🎸 Punk 기타 패턴 (8분음표 Downstroke)
PUNK_GUITAR_RHYTHM = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]


def get_punk_power_chord(chord):
    """🎸 Power Chord 변환 (C5, G5 → 루트 + 5도)"""

    # 🎯 리스트가 들어왔을 경우 첫 번째 값 사용
    if isinstance(chord, list):
        chord = chord[0]

        # 🎯 CHORD_TO_NOTES 에서 코드 가져오기
    if chord in CHORD_TO_NOTES:
        base_notes = CHORD_TO_NOTES[chord]
    else:
        print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 없음. 기본 C5 사용")
        base_notes = CHORD_TO_NOTES["C5"]  # 기본값

    # ✅ Power Chord = [루트, 5도]
    return [base_notes[0], base_notes[0] + 7]



def add_punk_guitar_track(midi, start_time, duration, chord_progression):
    """🎸 Punk Guitar 트랙 추가 (Power Chords & Downstroke)"""

    guitar_track = pretty_midi.Instrument(program=GUITAR_PROGRAM)

    for bar, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar * duration)

        power_chord = get_punk_power_chord(chord)  # ✅ Power Chord 변환


        for beat in PUNK_GUITAR_RHYTHM:
            beat_time = bar_start_time + (beat * (duration / 4))
            velocity = random.randint(90, 110)

            for note in power_chord:
                guitar_track.notes.append(pretty_midi.Note(
                    velocity=velocity,
                    pitch=note,
                    start=beat_time,
                    end=beat_time + 0.15  # 짧은 다운스트로크
                ))

    midi.instruments.append(guitar_track)