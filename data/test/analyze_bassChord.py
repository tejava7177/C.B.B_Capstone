import pretty_midi
from collections import defaultdict, Counter

# MIDI 프로그램 번호 기반 베이스 악기 목록
BASS_INSTRUMENTS = {32, 33, 34, 35, 36, 37, 38, 39}  # Acoustic, Fingered, Picked, Fretless, Slap, Synth Bass 등

# 코드 매핑 (근음을 기반으로 매칭)
ROOT_TO_CHORD = {
    0: "C Major", 1: "C#/Db Major", 2: "D Major", 3: "D#/Eb Major", 4: "E Major",
    5: "F Major", 6: "F#/Gb Major", 7: "G Major", 8: "G#/Ab Major", 9: "A Major",
    10: "A#/Bb Major", 11: "B Major"
}

def get_root_note_chord(notes):
    """가장 낮은 음 또는 가장 많이 등장한 음을 근음으로 설정하고 코드 추출"""
    if not notes:
        return "No Note"

    # 가장 낮은 음 또는 가장 많이 등장하는 음을 선택
    most_common_note, _ = Counter(notes).most_common(1)[0]  # 가장 많이 등장하는 음
    root_note = most_common_note % 12  # 음높이를 0~11 범위로 변환

    # 기본적으로 Major 코드로 설정 (예: C Major, D Major)
    return ROOT_TO_CHORD.get(root_note, f"Unknown Root({root_note})")

def analyze_bass_root_notes(midi_file, threshold=0.05):
    """베이스 악기의 근음을 기반으로 코드 진행 분석"""
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    bass_roots = defaultdict(list)  # 시간별 근음 저장

    print(f"\n🎸 {midi_file}의 베이스 라인 코드 분석 (근음 기반):\n")

    for instrument in midi_data.instruments:
        if instrument.program in BASS_INSTRUMENTS:  # 베이스 악기인지 확인
            instrument_name = pretty_midi.program_to_instrument_name(instrument.program)
            time_notes = defaultdict(list)  # 시간별 노트 그룹화

            # 노트들을 시간별로 그룹화
            for note in instrument.notes:
                time_notes[round(note.start / threshold) * threshold].append(note.pitch)

            # 근음을 코드로 변환
            for time, notes in sorted(time_notes.items()):
                chord_name = get_root_note_chord(notes)  # 가장 낮은 음을 근음으로 설정하여 코드 추출
                bass_roots[time].append(chord_name)

            # 베이스 악기별 코드 분석 결과 출력
            print(f"🎵 베이스 악기: {instrument_name} (Program: {instrument.program})")
            for time, chords in bass_roots.items():
                print(f"   ⏳ Time: {time:.2f}s -> Chord: {', '.join(chords)}")
            print("\n" + "-" * 50 + "\n")

# MIDI 파일 경로
midi_file_path = '/Volumes/Extreme SSD/lmd_aligned/O/C/D/TROCDKD128F92F128F/d52962c211dfebeffe92117855cffd3b.mid'

# 베이스 근음 코드 분석 실행
analyze_bass_root_notes(midi_file_path)