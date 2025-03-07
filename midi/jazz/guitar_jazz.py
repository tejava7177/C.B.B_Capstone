import pretty_midi
import random

# 🎸 기본 재즈 코드 보이싱 정의 (컴핑용)
JAZZ_CHORD_VOICINGS = {
    "Cmaj7": [48, 52, 55, 59],  # C E G B
    "Dm7": [50, 53, 57, 60],    # D F A C
    "G7": [43, 50, 53, 57],     # G B D F
    "Fmaj7": [41, 45, 48, 52],  # F A C E
    "Bm7": [47, 50, 54, 57],    # B D F# A
    "E7": [40, 47, 50, 54],     # E G# B D
    "Am7": [45, 48, 52, 55]     # A C E G
}

# 🎸 재즈 스케일 (즉흥 솔로용)
JAZZ_SCALES = {
    "Cmaj7": [48, 50, 52, 54, 55, 57, 59, 61],
    "Dm7": [50, 52, 53, 55, 57, 58, 60, 62],
    "G7": [43, 45, 47, 50, 52, 53, 55, 57],
    "Fmaj7": [41, 43, 45, 47, 48, 50, 52, 54],
    "Bm7": [47, 49, 50, 52, 54, 55, 57, 59],
    "E7": [40, 42, 44, 47, 49, 50, 52, 54],
    "Am7": [45, 47, 48, 50, 52, 53, 55, 57]
}

# 🎸 1. 자연스러운 코드 컴핑 (한 마디에 1~2번만 스트로크)


def add_jazz_guitar_comping(midi, start_time, duration, chord_progression):
    """🎸 재즈 기타 코드 컴핑 (더 부드러운 리듬과 스트로크 적용)"""

    guitar_comping = pretty_midi.Instrument(program=26)  # ✅ Clean Electric Guitar

    for bar, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar * duration)
        chord_notes = JAZZ_CHORD_VOICINGS.get(chord, JAZZ_CHORD_VOICINGS["Cmaj7"])

        # ✅ 코드 스트로크를 "한 번에" 울리지 않고, 시간차를 둠 (Rolled Chord)
        strum_delay = 0.02  # 한 음씩 미묘한 시간차를 둠
        velocity_variation = [random.randint(70, 90) for _ in chord_notes]

        for i, note in enumerate(chord_notes):
            guitar_comping.notes.append(pretty_midi.Note(
                velocity=velocity_variation[i],  # 🎵 강약 차이를 줌
                pitch=note,
                start=bar_start_time + (i * strum_delay),  # 🎵 줄을 하나씩 튕기는 효과
                end=bar_start_time + 0.3
            ))

        # ✅ 간혹 싱글 노트로 포인트를 주는 연주
        if random.random() > 0.6:
            point_note = random.choice(chord_notes)
            note_time = bar_start_time + random.uniform(0.3, duration - 0.2)
            guitar_comping.notes.append(pretty_midi.Note(
                velocity=random.randint(80, 100), pitch=point_note,
                start=note_time, end=note_time + 0.2
            ))

    midi.instruments.append(guitar_comping)


def generate_improvised_melody(chord, bar_start_time, duration):
    """🎶 재즈 솔로를 더 자연스럽게 - 해머온 & 슬라이드 추가"""

    scale_notes = JAZZ_CHORD_VOICINGS.get(chord, JAZZ_CHORD_VOICINGS["Cmaj7"])
    melody = []
    num_notes = random.randint(2, 5)  # 🎵 한 마디에 너무 많은 음을 넣지 않음

    for i in range(num_notes):
        note_pitch = random.choice(scale_notes)
        rhythm_choices = [0.15, 0.3, 0.45, 0.6, 0.75]  # 🎵 다양한 리듬 적용
        note_length = random.choice(rhythm_choices)
        note_start = bar_start_time + random.uniform(0.1, duration - note_length)
        note_end = note_start + note_length

        velocity = random.randint(65, 100)

        # ✅ 20% 확률로 해머온 & 풀오프 적용
        if random.random() > 0.8:
            next_pitch = note_pitch + random.choice([-2, 2])  # 반음 or 온음 차이
            melody.append(pretty_midi.Note(
                velocity=velocity, pitch=next_pitch, start=note_start + 0.05, end=note_end
            ))

        # ✅ 15% 확률로 슬라이드(Slide) 효과 적용
        if random.random() > 0.85 and melody:
            slide_pitch = note_pitch + random.choice([-3, 3])  # 슬라이드 업 or 다운
            slide_time = note_end - 0.1  # 슬라이드는 끝날 때 적용
            melody.append(pretty_midi.Note(
                velocity=velocity, pitch=slide_pitch, start=slide_time, end=note_end
            ))

        melody.append(pretty_midi.Note(
            velocity=velocity, pitch=note_pitch, start=note_start, end=note_end
        ))

    return melody

def add_jazz_guitar_solo(midi, start_time, duration, chord_progression):
    """🎸 재즈 기타 즉흥 솔로 (자연스러운 연주 스타일 적용)"""

    guitar_solo = pretty_midi.Instrument(program=26)  # ✅ Clean Electric Guitar

    for bar, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar * duration)
        melody = generate_improvised_melody(chord, bar_start_time, duration)
        guitar_solo.notes.extend(melody)

    midi.instruments.append(guitar_solo)