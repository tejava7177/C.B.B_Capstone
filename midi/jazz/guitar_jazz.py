import pretty_midi
import random
import sys

# ✅ CHORD_TO_NOTES 가져오기 (chord_map.py 활용)
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES

# 🎸 간결한 재즈 기타 리듬 패턴
JAZZ_GUITAR_RHYTHMS = [
    [0],  # 1박 (강한 첫 박)
    [0, 1.5],  # 1박 + 엇박
    [0, 2],  # 1, 3박
    [1, 2.5],  # 엇박 리듬
    [0, 2, 3],  # 1, 3, 4박
    [0, 1.5, 3],  # 스윙 스타일
]

# 🎸 기타 프로그램 변경 (Jazz Guitar로 설정)
GUITAR_PROGRAM = 33  # ✅ MIDI Program Number (27: Jazz Guitar)


def add_jazz_guitar_comping(midi, start_time, duration, chord_progression):
    """🎸 간결한 재즈 기타 코드 컴핑 (짧은 울림 & 리듬 브레이크 추가)"""

    guitar_comping = pretty_midi.Instrument(program=GUITAR_PROGRAM)  # ✅ Jazz Guitar

    for bar, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar * duration)
        chord_notes = CHORD_TO_NOTES.get(chord, CHORD_TO_NOTES["C Major"])

        # ✅ 랜덤한 리듬 패턴 선택 (자연스러운 간격 유지)
        rhythm_pattern = random.choice(JAZZ_GUITAR_RHYTHMS)

        for beat in rhythm_pattern:
            beat_time = bar_start_time + (beat * (duration / 4))
            beat_time += random.uniform(-0.05, 0.05)  # 미세한 박자 차이 적용

            # ✅ 코드의 일부 음만 선택해서 연주 (더 가벼운 느낌)
            selected_chord_notes = random.sample(chord_notes, k=random.randint(2, 3))

            # ✅ 강약 조절 (자연스러운 다이내믹)
            velocity_variation = [random.randint(70, 100) for _ in selected_chord_notes]

            for i, note in enumerate(selected_chord_notes):
                guitar_comping.notes.append(pretty_midi.Note(
                    velocity=velocity_variation[i],
                    pitch=note,
                    start=beat_time,
                    end=beat_time + random.uniform(0.2, 0.4)  # 🎵 짧은 울림 효과
                ))

        # ✅ 리듬 브레이크 추가 (랜덤하게 쉼표를 삽입)
        if random.random() > 0.8:
            rest_beat = random.choice([1, 2, 3])
            rest_time = bar_start_time + (rest_beat * (duration / 4))
            rest_end = rest_time + random.uniform(0.1, 0.2)  # 🎵 짧은 끊김 효과 추가

            silence_note = pretty_midi.Note(
                velocity=0, pitch=selected_chord_notes[0], start=rest_time, end=rest_end
            )
            guitar_comping.notes.append(silence_note)

    midi.instruments.append(guitar_comping)