# chord_to_notes.py
# 다양한 장르의 코드 노트를 포함한 매핑 파일

CHORD_TO_NOTES = {
    # Major Chords
    "CMajor": [60, 64, 67],
    "DMajor": [62, 66, 69],
    "EMajor": [64, 68, 71],
    "FMajor": [65, 69, 72],
    "GMajor": [67, 71, 74],
    "AMajor": [69, 73, 76],
    "BMajor": [71, 75, 78],

    # Minor Chords
    "CMinor": [60, 63, 67],
    "DMinor": [62, 65, 69],
    "EMinor": [64, 67, 71],
    "FMinor": [65, 68, 72],
    "GMinor": [67, 70, 74],
    "AMinor": [69, 72, 76],
    "BMinor": [71, 74, 78],

    # 7th Chords
    "C7": [60, 64, 67, 70],
    "D7": [62, 66, 69, 72],
    "E7": [64, 68, 71, 74],
    "F7": [65, 69, 72, 75],
    "G7": [67, 71, 74, 77],
    "A7": [69, 73, 76, 79],
    "B7": [71, 75, 78, 81],

    # Major 7th Chords
    "Cmaj7": [60, 64, 67, 71],
    "Dmaj7": [62, 66, 69, 73],
    "Emaj7": [64, 68, 71, 75],
    "Fmaj7": [65, 69, 72, 76],
    "Gmaj7": [67, 71, 74, 78],
    "Amaj7": [69, 73, 76, 80],
    "Bmaj7": [71, 75, 78, 82],

    # Minor 7th Chords
    "Cm7": [60, 63, 67, 70],
    "Dm7": [62, 65, 69, 72],
    "Em7": [64, 67, 71, 74],
    "Fm7": [65, 68, 72, 75],
    "Gm7": [67, 70, 74, 77],
    "Am7": [69, 72, 76, 79],
    "Bm7": [71, 74, 78, 81],

    # 9th Chords
    "C9": [60, 64, 67, 70, 74],
    "D9": [62, 66, 69, 72, 76],
    "E9": [64, 68, 71, 74, 78],
    "F9": [65, 69, 72, 75, 79],
    "G9": [67, 71, 74, 77, 81],
    "A9": [69, 73, 76, 79, 83],
    "B9": [71, 75, 78, 81, 85],

    # 13th Chords
    "C13": [60, 64, 67, 70, 74, 77, 81],
    "G13": [67, 71, 74, 77, 81, 84, 88],
    "D13": [62, 66, 69, 72, 76, 79, 83],

    # Suspended Chords
    "Asus4": [69, 74, 76],  # A - D - E
    "Bsus4": [71, 76, 78],  # B - E - F#
    "Csus4": [60, 65, 67],  # C - F - G
    "Dsus4": [62, 67, 69],  # D - G - A
    "Esus4": [64, 69, 71],  # E - A - B
    "Fsus4": [65, 70, 72],  # F - Bb - C
    "Gsus4": [67, 72, 74],  # G - C - D

    "Asus2": [69, 71, 76],  # A - B - E
    "Bsus2": [71, 73, 78],  # B - C# - F#
    "Csus2": [60, 62, 67],  # C - D - G
    "Dsus2": [62, 64, 69],  # D - E - A
    "Esus2": [64, 66, 71],  # E - F# - B
    "Fsus2": [65, 67, 72],  # F - G - C
    "Gsus2": [67, 69, 74],  # G - A - D

    # Diminished Chords
    "Adim": [69, 72, 75],  # A - C - Eb
    "Bdim": [71, 74, 77],  # B - D - F
    "Cdim": [60, 63, 66],  # C - Eb - Gb
    "Ddim": [62, 65, 68],  # D - F - Ab
    "Edim": [64, 67, 70],  # E - G - Bb
    "Fdim": [65, 68, 71],  # F - Ab - B
    "Gdim": [67, 70, 73],  # G - Bb - Db

    # Augmented Chords
    "Aaug": [69, 73, 77],  # A - C# - E#
    "Baug": [71, 75, 79],  # B - D# - G
    "Caug": [60, 64, 68],  # C - E - G#
    "Daug": [62, 66, 70],  # D - F# - A#
    "Eaug": [64, 68, 72],  # E - G# - C
    "Faug": [65, 69, 73],  # F - A - C#
    "Gaug": [67, 71, 75],  # G - B - D#

    # 6th Chords
    "C6": [60, 64, 67, 69],
    "G6": [67, 71, 74, 76],
    "E6": [64, 68, 71, 73],

    # 추가 코드
    "Cmaj9": [60, 64, 67, 71, 74],
    "Emaj9": [64, 68, 71, 75, 78],
    "Fmin9": [65, 68, 72, 75, 79],
    "B7b9": [71, 75, 78, 81, 84],


    # Power Chords (5th)
    "C5": [60, 67],   # C - G
    "D5": [62, 69],   # D - A
    "E5": [64, 71],   # E - B
    "F5": [65, 72],   # F - C
    "G5": [67, 74],   # G - D
    "A5": [69, 76],   # A - E
    "B5": [71, 78],   # B - F#
}
