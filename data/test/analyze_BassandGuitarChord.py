import pretty_midi
from collections import defaultdict, Counter

# MIDI 프로그램 번호 기반 악기 목록
BASS_INSTRUMENTS = {32, 33, 34, 35, 36, 37, 38, 39}  # 베이스 악기 (Acoustic, Fingered, Picked, Fretless 등)
GUITAR_INSTRUMENTS = {24, 25, 26, 27, 28, 29, 30, 31}  # 기타 악기 (Nylon, Steel, Electric, Distortion 등)

# 코드 매핑
CHORD_MAP = {
    (0, 4, 7): "C Major", (2, 6, 9): "D Major", (4, 8, 11): "E Major",
    (5, 9, 0): "F Major", (7, 11, 2): "G Major", (9, 1, 4): "A Major",
    (11, 3, 6): "B Major", (0, 3, 7): "C Minor", (2, 5, 9): "D Minor",
    (4, 7, 11): "E Minor", (5, 8, 0): "F Minor", (7, 10, 2): "G Minor",
    (9, 0, 3): "A Minor", (11, 2, 5): "B Minor",
}

# 루트 노트를 기반으로 기본 코드를 매칭 (기타 코드 부족 시 사용)
ROOT_TO_CHORD = {
    0: "C Major", 1: "C#/Db Major", 2: "D Major", 3: "D#/Eb Major", 4: "E Major",
    5: "F Major", 6: "F#/Gb Major", 7: "G Major", 8: "G#/Ab Major", 9: "A Major",
    10: "A#/Bb Major", 11: "B Major"
}

def get_chord_name(notes):
    """노트 리스트를 코드 이름으로 변환"""
    normalized_notes = sorted(set(note % 12 for note in notes))  # 음높이 정규화 (0~11)
    for chord_notes, chord_name in CHORD_MAP.items():
        if all(note in normalized_notes for note in chord_notes):
            return chord_name
    return None  # 코드 매칭 실패

def get_root_note_chord(notes):
    """가장 많이 등장하는 음을 근음으로 설정하고 코드 추출"""
    if not notes:
        return None
    most_common_note, _ = Counter(notes).most_common(1)[0]  # 가장 많이 등장하는 음
    root_note = most_common_note % 12  # 음높이를 0~11 범위로 변환
    return ROOT_TO_CHORD.get(root_note, f"Unknown Root({root_note})")

def analyze_bass_guitar_chords(midi_file, threshold=0.05):
    """베이스와 기타 악기의 코드 진행을 결합하여 분석"""
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    time_notes = defaultdict(lambda: {"bass": [], "guitar": []})  # 시간별 노트 저장

    print(f"\n🎸 {midi_file}의 베이스 + 기타 코드 진행 분석:\n")

    # 각 악기별 노트 추출
    for instrument in midi_data.instruments:
        instrument_name = pretty_midi.program_to_instrument_name(instrument.program)

        for note in instrument.notes:
            time = round(note.start / threshold) * threshold  # 일정 시간 간격으로 정렬

            if instrument.program in BASS_INSTRUMENTS:
                time_notes[time]["bass"].append(note.pitch)  # 베이스 음 저장
            elif instrument.program in GUITAR_INSTRUMENTS:
                time_notes[time]["guitar"].append(note.pitch)  # 기타 음 저장

    # 코드 분석 수행
    for time, notes in sorted(time_notes.items()):
        bass_notes = notes["bass"]
        guitar_notes = notes["guitar"]

        if guitar_notes:  # 기타 코드가 존재하는 경우
            chord_name = get_chord_name(guitar_notes)  # 기타 코드 분석
            if chord_name:
                print(f"   ⏳ Time: {time:.2f}s -> Chord: {chord_name} 🎸 (Based on Guitar)")
                continue  # 기타 코드가 있으면 그대로 사용

        if bass_notes:  # 기타 코드가 없고 베이스만 존재하는 경우
            chord_name = get_root_note_chord(bass_notes)  # 베이스 근음 분석
            print(f"   ⏳ Time: {time:.2f}s -> Chord: {chord_name} 🎸 (Based on Bass Root)")

# MIDI 파일 경로
midi_file_path = '/Volumes/Extreme SSD/lmd_aligned/O/C/D/TROCDKD128F92F128F/d52962c211dfebeffe92117855cffd3b.mid'

# 베이스 + 기타 코드 분석 실행
analyze_bass_guitar_chords(midi_file_path)