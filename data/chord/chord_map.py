# 🎯 코드 맵 & 코드 변환 관리 (새로운 파일)

# /data/chord/chord_map.py
""" 🎼 코드 진행을 매핑하는 파일 (CHORD_MAP & AUGMENTATION_MAP) """

CHORD_MAP = {
    # Major Triads (메이저 코드)
    (0, 4, 7): "CMajor",
    (2, 6, 9): "DMajor",
    (4, 8, 11): "EMajor",
    (5, 9, 0): "FMajor",
    (7, 11, 2): "GMajor",
    (9, 1, 4): "AMajor",
    (11, 3, 6): "BMajor",

    # Minor Triads (마이너 코드)
    (0, 3, 7): "CMinor",
    (2, 5, 9): "DMinor",
    (4, 7, 11): "EMinor",
    (5, 8, 0): "FMinor",
    (7, 10, 2): "GMinor",
    (9, 0, 3): "AMinor",
    (11, 2, 5): "BMinor",

    # Seventh Chords (7 코드)
    (0, 4, 7, 10): "C7",
    (2, 6, 9, 12): "D7",
    (4, 8, 11, 14): "E7",
    (5, 9, 0, 3): "F7",
    (7, 11, 2, 5): "G7",
    (9, 1, 4, 7): "A7",
    (11, 3, 6, 9): "B7",

    # Major 7th Chords (메이저 7 코드)
    (0, 4, 7, 11): "Cmaj7",
    (2, 6, 9, 1): "Dmaj7",
    (4, 8, 11, 2): "Emaj7",
    (5, 9, 0, 4): "Fmaj7",
    (7, 11, 2, 6): "Gmaj7",
    (9, 1, 4, 8): "Amaj7",
    (11, 3, 6, 10): "Bmaj7",

    # Minor 7th Chords (마이너 7 코드)
    (0, 3, 7, 10): "Cm7",
    (2, 5, 9, 12): "Dm7",
    (4, 7, 11, 14): "Em7",
    (5, 8, 0, 3): "Fm7",
    (7, 10, 2, 5): "Gm7",
    (9, 0, 3, 7): "Am7",
    (11, 2, 5, 9): "Bm7",

    # Suspended Chords (서스펜디드 코드)
    (0, 5, 7): "Csus4",
    (2, 7, 9): "Dsus4",
    (4, 9, 11): "Esus4",
    (5, 0, 2): "Fsus4",
    (7, 2, 4): "Gsus4",
    (9, 4, 6): "Asus4",
    (11, 6, 8): "Bsus4",

    # Add9 Chords (Add9 코드)
    (0, 4, 7, 14): "Cadd9",
    (2, 6, 9, 16): "Dadd9",
    (4, 8, 11, 18): "Eadd9",
    (5, 9, 0, 19): "Fadd9",
    (7, 11, 2, 21): "Gadd9",
    (9, 1, 4, 23): "Aadd9",
    (11, 3, 6, 25): "Badd9",

    # Diminished Chords (디미니쉬 코드)
    (0, 3, 6): "Cdim",
    (2, 5, 8): "Ddim",
    (4, 7, 10): "Edim",
    (5, 8, 11): "Fdim",
    (7, 10, 1): "Gdim",
    (9, 0, 3): "Adim",
    (11, 2, 5): "Bdim",

    # Augmented Chords (어그먼트 코드)
    (0, 4, 8): "Caug",
    (2, 6, 10): "Daug",
    (4, 8, 0): "Eaug",
    (5, 9, 1): "Faug",
    (7, 11, 3): "Gaug",
    (9, 1, 5): "Aaug",
    (11, 3, 7): "Baug"
}