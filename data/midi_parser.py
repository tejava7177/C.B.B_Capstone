import os
import json
import sys
import pretty_midi
from collections import defaultdict

# ✅ 프로젝트 루트 경로를 자동으로 추가 (C.B.B를 찾을 수 있도록)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ 이후에 모듈을 가져옴
from data.chord.chord_map import CHORD_MAP, AUGMENTATION_MAP


# MIDI 데이터셋 경로
MIDI_DATASET_PATH = "/Volumes/Extreme SSD/lmd_aligned"

# JSON 파일 저장 경로
OUTPUT_JSON_PATH = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord_melody_data.json"



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

def augment_chord(chord):
    """데이터셋에 없는 코드일 경우, 가장 유사한 코드로 변환"""
    return AUGMENTATION_MAP.get(chord, chord)  # 없으면 원래 코드 유지

def get_chord_name(notes):
    """노트 리스트를 코드 이름으로 변환"""
    normalized_notes = sorted(set(note % 12 for note in notes))
    for chord_notes, chord_name in CHORD_MAP.items():
        if all(note in normalized_notes for note in chord_notes):
            return augment_chord(chord_name)  # 🎯 새로운 코드 변환 적용
    return None

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
                if chord_name and chord_name != prev_chord:  # 중복 제거
                    chords.append(chord_name)
                    prev_chord = chord_name

        if not chords:
            print(f"⚠️ No chords found in: {midi_file}")  # ✅ MIDI에서 코드 진행이 추출되지 않았을 경우 로그 출력

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
                    print(f"🎵 {midi_path} → {chords}")  # ✅ MIDI에서 코드 진행 출력
                    midi_chord_data.append({"file_path": midi_path, "chords": chords})
                    count += 1
                else:
                    print(f"⚠️ No valid chords found in {midi_path}")

                # 최대 처리 개수 제한
                if count >= max_files:
                    break
        if count >= max_files:
            break

    print(f"✅ 총 {count}개의 MIDI 파일에서 코드 진행을 추출 완료!")
    return midi_chord_data

# MIDI 데이터셋에서 코드 진행 데이터 추출
midi_chord_data = process_all_midi_files(MIDI_DATASET_PATH, max_files=5000)

# ✅ JSON 저장 전에 리스트 크기 확인
print(f"🔍 midi_chord_data 크기: {len(midi_chord_data)}")

# ✅ 샘플 데이터 확인
if midi_chord_data:
    print(f"🔍 첫 번째 데이터 샘플: {json.dumps(midi_chord_data[0], indent=4)}")
else:
    print("⚠️ 추출된 코드 진행 데이터가 없습니다!")

# 데이터 저장
with open(OUTPUT_JSON_PATH, "w") as f:
    json.dump(midi_chord_data, f, indent=4)

print(f"✅ JSON 저장 완료: {OUTPUT_JSON_PATH}")