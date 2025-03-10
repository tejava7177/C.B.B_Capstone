import pretty_midi
import random

# 🎹 재즈 피아노 코드 보이싱 (싱글 노트와 조합)
JAZZ_PIANO_VOICINGS = {
    "Cmaj7": [48, 52, 55, 59, 62],  # C E G B D (9th 포함)
    "Dm7": [50, 53, 57, 60, 64],    # D F A C E
    "G7": [43, 50, 53, 57, 62],     # G B D F A
    "Fmaj7": [41, 45, 48, 52, 57],  # F A C E G
    "Bm7": [47, 50, 54, 57, 61],    # B D F# A C#
    "E7": [40, 47, 50, 54, 60],     # E G# B D F#
    "Am7": [45, 48, 52, 55, 59]     # A C E G B
}

# 🎹 재즈 피아노 싱글노트 스케일 (솔로 및 필인)
JAZZ_PIANO_SCALES = {
    "Cmaj7": [60, 62, 64, 65, 67, 69, 71, 72],
    "Dm7": [62, 64, 65, 67, 69, 71, 72, 74],
    "G7": [67, 69, 71, 72, 74, 76, 77, 79],
    "Fmaj7": [65, 67, 69, 70, 72, 74, 76, 77],
    "Bm7": [71, 73, 74, 76, 78, 80, 81, 83],
    "E7": [64, 66, 68, 69, 71, 73, 74, 76],
    "Am7": [69, 71, 72, 74, 76, 78, 79, 81]
}

# 🎹 랜덤한 리듬 패턴 (싱글노트 + 코드 조합)
PIANO_RHYTHM_PATTERNS = [
    [0, 2],  # 1, 3 박자
    [0, 1, 2],  # 1, 2, 3 박자
    [0, 3],  # 1, 4 박자
    [0, 1, 2, 3],  # 1, 2, 3, 4 박자
    [0, 1.5, 2.5],  # 스윙 스타일 엇박
    [0, 2, 2.75]  # 불규칙한 박자
]

# 🎹 재즈 피아노 트랙 추가 (연결감 + 레가토 포함)
def add_jazz_piano_track(midi, start_time, duration, chord_progression):
    """🎹 재즈 피아노 (싱글 노트 & 코드 컴핑 조합, 연결감 추가)"""

    piano = pretty_midi.Instrument(program=0)  # ✅ Acoustic Grand Piano

    previous_end_time = start_time  # 🎵 이전 노트의 종료 시간을 저장

    for bar, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar * duration)
        chord_notes = JAZZ_PIANO_VOICINGS.get(chord, JAZZ_PIANO_VOICINGS["Cmaj7"])
        scale_notes = JAZZ_PIANO_SCALES.get(chord, JAZZ_PIANO_SCALES["Cmaj7"])

        # ✅ 랜덤한 리듬 패턴 선택 (정박 70%, 엇박 30%)
        if random.random() < 0.7:
            rhythm_pattern = random.choice(PIANO_RHYTHM_PATTERNS[:4])  # 정박 위주 선택
        else:
            rhythm_pattern = random.choice(PIANO_RHYTHM_PATTERNS[4:])  # 엇박 선택

        for beat in rhythm_pattern:
            beat_time = bar_start_time + (beat * (duration / 4))
            beat_time += random.uniform(-0.05, 0.05)  # 박자 미세 조정

            # ✅ 50% 확률로 코드 / 50% 확률로 싱글노트 연주
            if random.random() > 0.5:
                # 🎹 코드 컴핑 연주 (조금 더 부드럽게)
                altered_chord = [n + random.choice([-2, 2]) if random.random() < 0.3 else n for n in chord_notes]
                velocity_variation = [random.randint(70, 100) for _ in altered_chord]
                for i, note in enumerate(altered_chord):
                    piano.notes.append(pretty_midi.Note(
                        velocity=velocity_variation[i],
                        pitch=note,
                        start=beat_time + (i * 0.02),  # 롤링 효과 적용
                        end=beat_time + 0.5  # 음을 조금 더 길게 늘려서 레가토 효과
                    ))
            else:
                # 🎵 싱글 노트 멜로디 추가 (연결감 추가)
                single_note = random.choice(scale_notes)
                note_length = random.choice([0.2, 0.3, 0.4, 0.6])  # 🎵 다양한 리듬 적용
                velocity = random.randint(65, 100)

                if beat_time < previous_end_time:
                    beat_time = previous_end_time + random.uniform(0.05, 0.1)  # ✅ 이전 음과 겹치지 않도록 조정

                previous_end_time = beat_time + note_length  # ✅ 다음 음의 시작점을 조정

                piano.notes.append(pretty_midi.Note(
                    velocity=velocity,
                    pitch=single_note,
                    start=beat_time,
                    end=beat_time + note_length
                ))

    midi.instruments.append(piano)