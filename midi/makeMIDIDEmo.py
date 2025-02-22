import pretty_midi

# 사용자가 제공한 코드맵
CHORD_MAP = {
    (0, 4, 7): "C Major", (2, 6, 9): "D Major", (4, 8, 11): "E Major",
    (5, 9, 0): "F Major", (7, 11, 2): "G Major", (9, 1, 4): "A Major",
    (11, 3, 6): "B Major", (0, 3, 7): "C Minor", (2, 5, 9): "D Minor",
    (4, 7, 11): "E Minor", (5, 8, 0): "F Minor", (7, 10, 2): "G Minor",
    (9, 0, 3): "A Minor", (11, 2, 5): "B Minor",
    (0, 4, 7, 10): "C7", (2, 6, 9, 12): "D7", (4, 8, 11, 14): "E7",
    (5, 9, 0, 3): "F7", (7, 11, 2, 5): "G7", (9, 1, 4, 7): "A7",
    (11, 3, 6, 9): "B7", (0, 4, 7, 11): "Cmaj7", (2, 6, 9, 1): "Dmaj7",
    (4, 8, 11, 2): "Emaj7", (5, 9, 0, 4): "Fmaj7", (7, 11, 2, 6): "Gmaj7",
    (9, 1, 4, 8): "Amaj7", (11, 3, 6, 10): "Bmaj7",
    (0, 3, 7, 10): "Cm7", (2, 5, 9, 12): "Dm7", (4, 7, 11, 14): "Em7",
    (5, 8, 0, 3): "Fm7", (7, 10, 2, 5): "Gm7", (9, 0, 3, 7): "Am7",
    (11, 2, 5, 9): "Bm7", (0, 5, 7): "Csus4", (2, 7, 9): "Dsus4",
    (4, 9, 11): "Esus4", (5, 0, 2): "Fsus4", (7, 2, 4): "Gsus4",
    (9, 4, 6): "Asus4", (11, 6, 8): "Bsus4",
    (0, 4, 7, 14): "Cadd9", (2, 6, 9, 16): "Dadd9", (4, 8, 11, 18): "Eadd9",
    (5, 9, 0, 19): "Fadd9", (7, 11, 2, 21): "Gadd9", (9, 1, 4, 23): "Aadd9",
    (11, 3, 6, 25): "Badd9", (0, 3, 6): "Cdim", (2, 5, 8): "Ddim",
    (4, 7, 10): "Edim", (5, 8, 11): "Fdim", (7, 10, 1): "Gdim",
    (9, 0, 3): "Adim", (11, 2, 5): "Bdim",
    (0, 4, 8): "Caug", (2, 6, 10): "Daug", (4, 8, 0): "Eaug",
    (5, 9, 1): "Faug", (7, 11, 3): "Gaug", (9, 1, 5): "Aaug",
    (11, 3, 7): "Baug"
}

# 코드 이름을 MIDI 노트 리스트로 변환
# CHORD_TO_NOTES = {
#     "C Major": [60, 64, 67], "G Major": [55, 59, 62], "A Minor": [57, 60, 64],
#     "F Major": [53, 57, 60], "D Minor": [50, 53, 57], "E Major": [52, 56, 59],
#     "B Minor": [47, 50, 54], "Cmaj7": [60, 64, 67, 71], "G7": [55, 59, 62, 65],
#     "D7": [50, 54, 57, 60], "E7": [52, 56, 59, 62]
# }


# 🎼 CHORD_TO_NOTES 확장 (9th, sus4, maj7 추가)
CHORD_TO_NOTES = {
    # ✅ Major Chords
    "C Major": [60, 64, 67], "G Major": [55, 59, 62], "A Major": [57, 61, 64],
    "F Major": [53, 57, 60], "D Major": [50, 54, 57], "E Major": [52, 56, 59],
    "B Major": [47, 51, 54],

    # ✅ Minor Chords
    "C Minor": [60, 63, 67], "G Minor": [55, 58, 62], "A Minor": [57, 60, 64],
    "F Minor": [53, 56, 60], "D Minor": [50, 53, 57], "E Minor": [52, 55, 59],
    "B Minor": [47, 50, 54],

    # ✅ Seventh Chords (7th)
    "C7": [60, 64, 67, 70], "G7": [55, 59, 62, 65], "D7": [50, 54, 57, 60],
    "E7": [52, 56, 59, 62], "A7": [57, 61, 64, 67], "B7": [47, 51, 54, 57],

    # ✅ Major 7th Chords (maj7)
    "Cmaj7": [60, 64, 67, 71], "Gmaj7": [55, 59, 62, 66], "Dmaj7": [50, 54, 57, 61],
    "Emaj7": [52, 56, 59, 63], "Amaj7": [57, 61, 64, 68], "Bmaj7": [47, 51, 54, 58],

    # ✅ 9th Chords (9)
    "C9": [60, 64, 67, 70, 74], "G9": [55, 59, 62, 65, 69], "F9": [53, 57, 60, 63, 67],
    "D9": [50, 54, 57, 60, 64], "A9": [57, 61, 64, 67, 71],

    # ✅ Suspended Chords (sus4)
    "Csus4": [60, 65, 67], "Gsus4": [55, 60, 62], "Dsus4": [50, 55, 57],

    # ✅ Augmented Chords (aug)
    "Caug": [60, 64, 68], "Gaug": [55, 59, 63], "Daug": [50, 54, 58],

    # ✅ Diminished Chords (dim)
    "Cdim": [60, 63, 66], "Gdim": [55, 58, 61], "Ddim": [50, 53, 56],

    # ✅ Bsus4 추가
    "Bsus4": [47, 52, 54]
}


def save_chord_progression_to_midi(chord_progression, bpm=120, filename="output.mid"):
    """AI가 생성한 코드 진행을 MIDI 파일로 변환 (4박자로 설정)"""

    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    start_time = 0.0
    beats_per_second = bpm / 60.0  # BPM을 초 단위로 변환
    chord_duration = 4 / beats_per_second  # 4박자 지속 시간

    for chord in chord_progression:
        midi_notes = CHORD_TO_NOTES.get(chord, [60, 64, 67])  # 코드 노트 변환

        for note_number in midi_notes:
            note = pretty_midi.Note(velocity=100, pitch=note_number, start=start_time, end=start_time + chord_duration)
            instrument.notes.append(note)

        start_time += chord_duration  # 다음 코드로 진행

    midi.instruments.append(instrument)
    midi.write(filename)
    print(f"✅ MIDI 파일이 생성되었습니다: {filename}")


# 🎵 AI가 생성한 코드 진행 (샘플)
ai_generated_chords = ["C9", "G9", "F9", "E7", "G9", "E Major","G9","Amaj7", "Cmaj7", "Bsus4", "Dmaj7", "D9", "Amaj7", "Dmaj7", "B7"]

# MIDI 파일 생성 (4박자 적용)
save_chord_progression_to_midi(ai_generated_chords, bpm=120, filename="ai_generated_chords_4beats.mid")