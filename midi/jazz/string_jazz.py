import pretty_midi
import random
import sys

# ✅ CHORD_TO_NOTES 가져오기 (chord_map.py 활용)
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES

# 🎻 현악기 프로그램 번호 (MIDI Standard)
STRINGS_PROGRAMS = {
    "violin": 40,   # Violin
    "viola": 41,    # Viola
    "cello": 42,    # Cello
    "bass": 43      # Contrabass
}

# ✅ 부드러운 코드 패드 패턴
STRING_PATTERNS = [
    [0],  # 첫 박자에서 연주 후 유지
    [0, 3],  # 첫 박자와 넷째 박자에서 연주
]

def get_string_voicing(chord):
    """🎵 코드에 맞는 현악기 보이싱 생성"""
    if chord in CHORD_TO_NOTES:
        base_notes = CHORD_TO_NOTES[chord]  # 기본 코드 음표 가져오기
    else:
        print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 없음. 기본 Cmaj7 사용")
        base_notes = CHORD_TO_NOTES["Cmaj7"]

    # 🎻 루트, 5도, 7도, 9도 구성 (4성부)
    if len(base_notes) >= 3:
        return [
            base_notes[0] - 12,  # 저음 (첼로)
            base_notes[0],  # 루트 (콘트라베이스)
            base_notes[1],  # 3도 (비올라)
            base_notes[2]   # 5도 (바이올린)
        ]
    return base_notes

def add_jazz_strings_track(midi, start_time, duration, chord_progression):
    """🎻 재즈 현악기 코드 패드 트랙 추가"""

    # ✅ 악기별 트랙 생성
    violin = pretty_midi.Instrument(program=STRINGS_PROGRAMS["violin"])  # 🎻 바이올린
    viola = pretty_midi.Instrument(program=STRINGS_PROGRAMS["viola"])  # 🎻 비올라
    cello = pretty_midi.Instrument(program=STRINGS_PROGRAMS["cello"])  # 🎻 첼로
    bass = pretty_midi.Instrument(program=STRINGS_PROGRAMS["bass"])  # 🎻 콘트라베이스

    for bar, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar * duration)
        chord_notes = get_string_voicing(chord)  # ✅ 현악 보이싱 가져오기

        # ✅ 랜덤한 연주 패턴 선택 (박자 변형)
        rhythm_pattern = random.choice(STRING_PATTERNS)

        for beat in rhythm_pattern:
            beat_time = bar_start_time + (beat * (duration / 4))
            beat_time += random.uniform(-0.05, 0.05)  # 🎵 박자 랜덤 딜레이

            # 🎻 각 악기별 노트 추가
            bass.notes.append(pretty_midi.Note(
                velocity=random.randint(60, 75),
                pitch=chord_notes[0],  # 🎻 루트음
                start=beat_time,
                end=beat_time + duration * 0.9
            ))

            cello.notes.append(pretty_midi.Note(
                velocity=random.randint(65, 80),
                pitch=chord_notes[1],  # 🎻 루트음 (옥타브 높은 첼로)
                start=beat_time,
                end=beat_time + duration * 0.85
            ))

            viola.notes.append(pretty_midi.Note(
                velocity=random.randint(70, 85),
                pitch=chord_notes[2],  # 🎻 3도 (비올라)
                start=beat_time + random.uniform(0.02, 0.1),
                end=beat_time + duration * 0.8
            ))

            violin.notes.append(pretty_midi.Note(
                velocity=random.randint(75, 90),
                pitch=chord_notes[3],  # 🎻 5도 (바이올린)
                start=beat_time + random.uniform(0.05, 0.12),
                end=beat_time + duration * 0.75
            ))

    # ✅ MIDI 트랙에 추가
    midi.instruments.append(violin)
    midi.instruments.append(viola)
    midi.instruments.append(cello)
    midi.instruments.append(bass)