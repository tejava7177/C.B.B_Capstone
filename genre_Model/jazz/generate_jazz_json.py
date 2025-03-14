import os
import json
import pretty_midi

# ✅ 재즈 JSON 파일 및 모델 저장 디렉토리 설정
JAZZ_DIR = "/Volumes/Extreme SSD/lmd_classified/jazz"
SAVE_DIR = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz"

# ✅ 저장 디렉토리 생성
os.makedirs(SAVE_DIR, exist_ok=True)


def extract_jazz_features(midi_path):
    """🎷 MIDI 파일에서 재즈 코드 진행, 멜로디, 리듬 패턴 및 주요 악기 추출"""
    try:
        if midi_path.startswith("._"):  # ✅ 숨김 파일(._) 무시
            print(f"🛑 무시된 파일: {midi_path}")
            return None

        midi_data = pretty_midi.PrettyMIDI(midi_path)

        chords, melody, rhythm_pattern = [], [], []
        instruments = set()

        for instrument in midi_data.instruments:
            if not instrument.is_drum:
                instruments.add(instrument.name)  # 🎺 주요 악기 저장

                for note in instrument.notes:
                    melody.append(note.pitch)
                    rhythm_pattern.append(1 if note.velocity > 0 else 0)

                # 코드 진행 추출 (첫 3개 노트 기반)
                if len(instrument.notes) >= 3:
                    chords.append(instrument.notes[0].pitch)

        return {
            "chords": chords[:10],  # 🎼 10개까지만 저장
            "melody": melody[:10],
            "rhythm_pattern": rhythm_pattern[:10],
            "instrument": list(instruments)
        }

    except Exception as e:
        print(f"⚠️ 오류 발생: {midi_path} - {e}")
        if os.path.exists(midi_path):  # ✅ 파일이 존재할 때만 삭제
            os.remove(midi_path)
            print(f"🗑️ 삭제 완료: {midi_path}")
        return None


def process_jazz():
    """🎵 재즈 장르 MIDI 파일 처리 & JSON 변환"""
    midi_data_list = []

    for midi_file in os.listdir(JAZZ_DIR):
        if midi_file.endswith(".mid"):
            midi_path = os.path.join(JAZZ_DIR, midi_file)
            features = extract_jazz_features(midi_path)
            if features:
                features["midi_file"] = midi_file
                midi_data_list.append(features)

    return midi_data_list


# ✅ JSON 파일 저장
jazz_data = {"jazz": process_jazz()}
json_path = os.path.join(SAVE_DIR, "jazz_dataset.json")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(jazz_data, f, indent=4)

print(f"✅ JSON 데이터 저장 완료: {json_path}")