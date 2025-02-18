import os
import pretty_midi
from collections import defaultdict
import json

# MIDI 데이터셋 경로
MIDI_DATASET_PATH = "/Volumes/Extreme SSD/lmd_aligned"

# 코드 매핑 테이블
CHORD_MAP = {
    (0, 4, 7): "C Major", (2, 6, 9): "D Major", (4, 8, 11): "E Major",
    (5, 9, 0): "F Major", (7, 11, 2): "G Major", (9, 1, 4): "A Major",
    (11, 3, 6): "B Major", (0, 3, 7): "C Minor", (2, 5, 9): "D Minor",
    (4, 7, 11): "E Minor", (5, 8, 0): "F Minor", (7, 10, 2): "G Minor",
    (9, 0, 3): "A Minor", (11, 2, 5): "B Minor",
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
    normalized_notes = sorted(set(note % 12 for note in notes))  # 0~11 범위로 변환
    for chord_notes, chord_name in CHORD_MAP.items():
        if all(note in normalized_notes for note in chord_notes):
            return chord_name
    return None  # 매칭되는 코드가 없을 경우

def extract_chords_from_midi(midi_file):
    """MIDI 파일에서 코드 진행을 추출"""
    try:
        midi_data = pretty_midi.PrettyMIDI(midi_file)
        time_notes = defaultdict(list)

        # 모든 노트를 시간별로 그룹화
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                time_notes[round(note.start, 2)].append(note.pitch)

        # 시간별 코드 분석
        chords = []
        prev_chord = None  # 중복 코드 제거를 위한 변수
        for time, notes in sorted(time_notes.items()):
            if len(notes) >= 3:  # 코드로 인식하려면 최소 3개의 노트 필요
                chord_name = get_chord_name(notes)
                if chord_name and chord_name != prev_chord:
                    chords.append(chord_name)
                    prev_chord = chord_name  # 연속적인 코드 중복 방지

        return chords if len(chords) > 1 else None  # 너무 짧은 코드 진행은 무시
    except Exception as e:
        print(f"❌ MIDI 파일 처리 오류: {midi_file} - {e}")
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
output_json_path = "../dataset/midi_chord_data.json"
with open(output_json_path, "w") as f:
    json.dump(midi_chord_data, f, indent=4)

print(f"✅ 총 {len(midi_chord_data)}개의 MIDI 파일에서 코드 진행을 추출 완료!")