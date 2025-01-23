import pretty_midi
from collections import defaultdict

# MIDI 노트를 코드 이름으로 매핑
CHORD_MAP = {
    (0, 4, 7): "C Major",
    (0, 3, 7): "C Minor",
    (2, 5, 9): "D Minor",
    (4, 7, 11): "E Major",
    (5, 9, 0): "F Major",
    (7, 11, 2): "G Major",
    (9, 0, 4): "A Minor",
    (11, 2, 5): "B Diminished"
    # 필요하면 다른 코드 조합 추가
}

def get_chord_name(notes):
    """노트 리스트를 코드 이름으로 변환"""
    normalized_notes = sorted(set(note % 12 for note in notes))  # 음높이 정규화 (0~11)
    for chord_notes, chord_name in CHORD_MAP.items():
        if all(note in normalized_notes for note in chord_notes):
            return chord_name
    return f"Unknown({normalized_notes})"  # 매핑되지 않은 코드

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
            chords.append((time, chord_name))

    return chords

# MIDI 파일에서 코드 추출
midi_file_path = '/Volumes/Extreme SSD/lmd_aligned/O/F/F/TROFFYZ128F429262A/279ab4352b18622af04183c069537e4e.mid'
chords = midi_to_chords(midi_file_path)

# 결과 출력
for time, chord in chords:
    print(f"Time: {time:.2f}s, Chord: {chord}")