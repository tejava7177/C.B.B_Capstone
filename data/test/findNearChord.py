import pretty_midi
from collections import defaultdict

# MIDI 노트를 코드 이름으로 매핑 (0~11 범위)
CHORD_MAP = {
    # Major Triads (메이저 코드)
    (0, 4, 7): "C Major",
    (2, 6, 9): "D Major",
    (4, 8, 11): "E Major",
    (5, 9, 0): "F Major",
    (7, 11, 2): "G Major",
    (9, 1, 4): "A Major",
    (11, 3, 6): "B Major",

    # Minor Triads (마이너 코드)
    (0, 3, 7): "C Minor",
    (2, 5, 9): "D Minor",
    (4, 7, 11): "E Minor",
    (5, 8, 0): "F Minor",
    (7, 10, 2): "G Minor",
    (9, 0, 3): "A Minor",
    (11, 2, 5): "B Minor",

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
}


def get_chord_name(notes):
    """노트 리스트를 코드 이름으로 변환"""
    normalized_notes = sorted(set(note % 12 for note in notes))  # 음높이 정규화 (0~11)

    for chord_notes, chord_name in CHORD_MAP.items():
        if all(note in normalized_notes for note in chord_notes):
            return chord_name

    return f"Unknown({normalized_notes})"  # 매핑되지 않은 코드


def get_closest_chord(notes):
    """Unknown 코드일 경우, 가장 유사한 코드 찾기"""
    normalized_notes = sorted(set(note % 12 for note in notes))  # 음높이 정규화
    best_match = None
    best_match_score = 0

    for chord_notes, chord_name in CHORD_MAP.items():
        chord_notes_set = set(chord_notes)
        matched_notes = len(chord_notes_set.intersection(normalized_notes))  # 매칭된 노트 개수

        if matched_notes > best_match_score:
            best_match = chord_name
            best_match_score = matched_notes

    return best_match if best_match else None


def midi_to_chords(midi_file, threshold=0.05):
    """MIDI 파일에서 코드를 추출"""
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    chords = []
    time_notes = defaultdict(list)  # 시간별 노트 그룹화

    # 노트 정보를 시간별로 그룹화
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            time_notes[round(note.start / threshold) * threshold].append(note.pitch)

    # 그룹화된 노트들을 코드로 변환
    for time, notes in sorted(time_notes.items()):
        if len(notes) > 2:  # 코드로 해석 가능한 노트만 처리
            chord_name = get_chord_name(notes)

            # Unknown 코드일 경우, 가장 가까운 코드 추천
            if "Unknown" in chord_name:
                closest_chord = get_closest_chord(notes)
                if closest_chord:
                    chord_name = f"{chord_name} (Maybe: {closest_chord})"

            chords.append((time, chord_name))

    return chords


# MIDI 파일에서 코드 추출
midi_file_path = '/Volumes/Extreme SSD/lmd_aligned/M/N/O/TRMNOKT128F930E066/f939de5d931efb02350769ac5437e6f5.mid'
chords = midi_to_chords(midi_file_path)

# 결과 출력
for time, chord in chords:
    print(f"Time: {time:.2f}s, Chord: {chord}")