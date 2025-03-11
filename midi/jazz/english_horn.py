import pretty_midi
import random
import sys

# ✅ CHORD_TO_NOTES 가져오기 (chord_map.py 활용)
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES

# 🎶 잉글리쉬 호른 프로그램 번호 (MIDI Standard)
ENGLISH_HORN_PROGRAM = 69  # 🎻 English Horn

# 🎵 멜로디 리듬 패턴 (부드러운 스타일)
HORN_RHYTHM_PATTERNS = [
    [0, 2],       # 🎵 첫 박자 + 셋째 박자 연주
    [0, 1.5, 3],  # 🎵 싱코페이션 포함 패턴
    [0, 2.5]      # 🎵 루바토 스타일 (약간의 자유로운 박자)
]

def get_horn_melody_scale(chord):
    """🎻 코드에 맞는 잉글리쉬 호른 멜로디 스케일 생성"""
    if chord in CHORD_TO_NOTES:
        base_notes = CHORD_TO_NOTES[chord]  # 기본 코드 음표 가져오기
    else:
        print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 없음. 기본 Cmaj7 사용")
        base_notes = CHORD_TO_NOTES["Cmaj7"]

    # ✅ 멜로디 스케일 (3도, 5도, 7도, 9도 활용)
    if len(base_notes) >= 3:
        return [
            base_notes[0] + 12,  # 🎻 루트 음 (옥타브 올림)
            base_notes[1] + 12,  # 🎻 3도
            base_notes[2] + 12,  # 🎻 5도
            base_notes[0] + 14,  # 🎻 9도 (확장 코드)
        ]
    return base_notes

def add_jazz_horn_track(midi, start_time, duration, chord_progression):
    """🎻 재즈 잉글리쉬 호른 멜로디 트랙 추가"""

    horn = pretty_midi.Instrument(program=ENGLISH_HORN_PROGRAM)  # 🎻 English Horn

    for bar, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar * duration)
        melody_scale = get_horn_melody_scale(chord)  # ✅ 코드 기반 스케일 가져오기

        # ✅ 랜덤한 리듬 패턴 선택
        rhythm_pattern = random.choice(HORN_RHYTHM_PATTERNS)

        for beat in rhythm_pattern:
            beat_time = bar_start_time + (beat * (duration / 4))
            beat_time += random.uniform(-0.05, 0.05)  # 🎵 박자 랜덤 딜레이

            note_pitch = random.choice(melody_scale)  # 🎻 멜로디 스케일에서 노트 선택
            note_length = random.uniform(0.4, 0.8)  # 🎵 길이 랜덤 적용 (더 길게 유지)
            velocity = random.randint(75, 100)  # 🎵 강약 조절

            horn.notes.append(pretty_midi.Note(
                velocity=velocity,
                pitch=note_pitch,
                start=beat_time,
                end=beat_time + note_length
            ))

            # 🎻 글리산도(Glissando) & 벤딩 효과 추가
            if random.random() > 0.7:  # ✅ 70% 확률로 적용
                slide_pitch = note_pitch + random.choice([-2, 2])  # 반음 or 온음 차이
                slide_time = beat_time + note_length - 0.1
                horn.notes.append(pretty_midi.Note(
                    velocity=velocity,
                    pitch=slide_pitch,
                    start=slide_time,
                    end=beat_time + note_length
                ))

    midi.instruments.append(horn)
    return horn  # ✅ 생성한 호른 트랙 반환