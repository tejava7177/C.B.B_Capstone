# 🎯 코드 맵 & 코드 변환 관리 (새로운 파일)

# /data/chord/chord_map.py
""" 🎼 코드 진행을 매핑하는 파일 (CHORD_MAP & AUGMENTATION_MAP) """

# ✅ 코드 매핑 (Major, Minor, 7th, dim, aug, sus, add9 포함)
CHORD_MAP = {
    (0, 4, 7): "C Major", (2, 6, 9): "D Major", (4, 8, 11): "E Major",
    (5, 9, 0): "F Major", (7, 11, 2): "G Major", (9, 1, 4): "A Major",
    (11, 3, 6): "B Major",
    (0, 3, 7): "C Minor", (2, 5, 9): "D Minor", (4, 7, 11): "E Minor",
    (5, 8, 0): "F Minor", (7, 10, 2): "G Minor", (9, 0, 3): "A Minor",
    (11, 2, 5): "B Minor",
    (0, 4, 7, 10): "C7", (2, 6, 9, 12): "D7", (4, 8, 11, 14): "E7",
    (5, 9, 0, 3): "F7", (7, 11, 2, 5): "G7", (9, 1, 4, 7): "A7",
    (11, 3, 6, 9): "B7",
    (0, 4, 7, 11): "Cmaj7", (2, 6, 9, 1): "Dmaj7", (4, 8, 11, 2): "Emaj7",
    (5, 9, 0, 4): "Fmaj7", (7, 11, 2, 6): "Gmaj7", (9, 1, 4, 8): "Amaj7",
    (11, 3, 6, 10): "Bmaj7",
    (0, 3, 7, 10): "Cm7", (2, 5, 9, 12): "Dm7", (4, 7, 11, 14): "Em7",
    (5, 8, 0, 3): "Fm7", (7, 10, 2, 5): "Gm7", (9, 0, 3, 7): "Am7",
    (11, 2, 5, 9): "Bm7",
    (0, 2, 7): "Csus2", (2, 4, 9): "Dsus2", (4, 6, 11): "Esus2",
    (5, 7, 0): "Fsus2", (7, 9, 2): "Gsus2", (9, 11, 4): "Asus2",
    (11, 1, 6): "Bsus2",
    (0, 5, 7): "Csus4", (2, 7, 9): "Dsus4", (4, 9, 11): "Esus4",
    (5, 0, 2): "Fsus4", (7, 2, 4): "Gsus4", (9, 4, 6): "Asus4",
    (11, 6, 8): "Bsus4",
    (0, 4, 8): "Caug", (2, 6, 10): "Daug", (4, 8, 0): "Eaug",
    (5, 9, 1): "Faug", (7, 11, 3): "Gaug", (9, 1, 5): "Aaug",
    (11, 3, 7): "Baug",
}

# ✅ 코드 변환 (데이터셋에 없는 코드 변환)
AUGMENTATION_MAP = {
    "Cmaj9": "Cmaj7", "Fmaj9": "Fmaj7", "G13": "G7",
    "A7sus4": "A7", "D9": "D7", "E7sus4": "E7",
    "Cmin9": "Cm7", "Fmin9": "Fm7", "Gmin11": "Gm7",
    "Csus2": "C Major", "Gsus2": "G Major",
    "Cdim7": "Cdim", "Gdim7": "Gdim",
    "Cadd9": "C Major", "Gadd9": "G Major"
}