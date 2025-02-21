import os
import json
import pretty_midi
from collections import defaultdict

# MIDI 데이터셋 경로
MIDI_DATASET_PATH = "/Volumes/Extreme SSD/lmd_aligned"

# JSON 파일 저장 경로
OUTPUT_JSON_PATH = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/model/dataset/midi_chord_data.json"

# 코드 매핑 테이블 (다양한 코드 포함)
CHORD_MAP = {
    # Major Triads
    (0, 4, 7): "C Major", (2, 6, 9): "D Major", (4, 8, 11): "E Major",
    (5, 9, 0): "F Major", (7, 11, 2): "G Major", (9, 1, 4): "A Major",
    (11, 3, 6): "B Major",

    # Minor Triads
    (0, 3, 7): "C Minor", (2, 5, 9): "D Minor", (4, 7, 11): "E Minor",
    (5, 8, 0): "F Minor", (7, 10, 2): "G Minor", (9, 0, 3): "A Minor",
    (11, 2, 5): "B Minor",

    # 7th Chords
    (0, 4, 7, 10): "C7", (2, 6, 9, 12): "D7", (4, 8, 11, 14): "E7",
    (5, 9, 0, 3): "F7", (7, 11, 2, 5): "G7", (9, 1, 4, 7): "A7",
    (11, 3, 6, 9): "B7",

    # Major 7th
    (0, 4, 7, 11): "Cmaj7", (2, 6, 9, 1): "Dmaj7", (4, 8, 11, 2): "Emaj7",
    (5, 9, 0, 4): "Fmaj7", (7, 11, 2, 6): "Gmaj7", (9, 1, 4, 8): "Amaj7",
    (11, 3, 6, 10): "Bmaj7",

    # Suspended Chords
    (0, 5, 7): "Csus4", (2, 7, 9): "Dsus4", (4, 9, 11): "Esus4",
    (5, 0, 2): "Fsus4", (7, 2, 4): "Gsus4", (9, 4, 6): "Asus4",
    (11, 6, 8): "Bsus4",

    # Diminished & Augmented Chords
    (0, 3, 6): "Cdim", (2, 5, 8): "Ddim", (4, 7, 10): "Edim",
    (5, 8, 11): "Fdim", (7, 10, 1): "Gdim", (9, 0, 3): "Adim",
    (11, 2, 5): "Bdim",

    (0, 4, 8): "Caug", (2, 6, 10): "Daug", (4, 8, 0): "Eaug",
    (5, 9, 1): "Faug", (7, 11, 3): "Gaug", (9, 1, 5): "Aaug",
    (11, 3, 7): "Baug"
}

def is_valid_midi_file(file_path):
    """MIDI 파일이 정상적인지 확인"""
    if file_path.startswith("._"):  # macOS 숨김 파일 무시
        return False
    try:
        with open(file_path, "rb") as f:
            header = f.read(4)
            return header == b"MThd"  # MIDI 파일의 올바른 헤더 확인
    except Exception:
        return False

def get_chord_name(notes):
    """노트 리스트를 코드 이름으로 변환"""
    normalized_notes = sorted(set(note % 12 for note in notes))
    for chord_notes, chord_name in CHORD_MAP.items():
        if all(note in normalized_notes for note in chord_notes):
            return chord_name
    return None

def get_closest_chord(notes):
    """Unknown 코드일 경우, 가장 유사한 코드 찾기"""
    normalized_notes = sorted(set(note % 12 for note in notes))
    best_match = None
    best_match_score = 0
    for chord_notes, chord_name in CHORD_MAP.items():
        matched_notes = len(set(chord_notes).intersection(normalized_notes))
        if matched_notes > best_match_score:
            best_match = chord_name
            best_match_score = matched_notes
    return best_match if best_match else None

def extract_chords_from_midi(midi_file):
    """MIDI 파일에서 코드 진행을 추출"""
    try:
        midi_data = pretty_midi.PrettyMIDI(midi_file)
        time_notes = defaultdict(list)
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                time_notes[round(note.start, 2)].append(note.pitch)

        chords = []
        prev_chord = None  # 중복 코드 제거용
        for time, notes in sorted(time_notes.items()):
            if len(notes) >= 3:
                chord_name = get_chord_name(notes)
                if not chord_name:  # Unknown 코드일 경우, 가장 가까운 코드 추천
                    chord_name = get_closest_chord(notes)
                if chord_name and chord_name != prev_chord:  # 중복 제거
                    chords.append(chord_name)
                    prev_chord = chord_name

        return chords if len(chords) > 1 else None
    except Exception as e:
        print(f"❌ MIDI 처리 오류: {midi_file} - {e}")
        return None

def process_all_midi_files(dataset_path, max_files=5000):
    """데이터셋 전체에서 MIDI 파일을 검색하고 코드 진행을 추출"""
    midi_chord_data = []
    count = 0

    for root, _, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(".mid") or file.endswith(".midi"):
                midi_path = os.path.join(root, file)

                # MIDI 파일이 정상적인지 검사
                if not is_valid_midi_file(midi_path):
                    print(f"⚠️  Skipping invalid MIDI file: {midi_path}")
                    continue

                chords = extract_chords_from_midi(midi_path)

                if chords:
                    midi_chord_data.append({"file_path": midi_path, "chords": chords})
                    count += 1

                # 최대 처리 개수 제한
                if count >= max_files:
                    break
        if count >= max_files:
            break

    return midi_chord_data

# MIDI 데이터셋에서 코드 진행 데이터 추출
midi_chord_data = process_all_midi_files(MIDI_DATASET_PATH, max_files=5000)

# 데이터 저장
with open(OUTPUT_JSON_PATH, "w") as f:
    json.dump(midi_chord_data, f, indent=4)

print(f"✅ 총 {len(midi_chord_data)}개의 MIDI 파일에서 코드 진행을 추출 완료!")