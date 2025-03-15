import os
import json
import pretty_midi

# ✅ MIDI 파일 및 데이터셋 디렉토리 설정
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

        # ✅ 템포 가져오기 (트랙에서 직접 추출하는 방식 변경)
        estimated_tempo = midi_data.estimate_tempo()
        if len(midi_data.get_tempo_changes()[1]) > 0:  # 템포 변경 이벤트 존재 여부 확인
            tempo = midi_data.get_tempo_changes()[1][0]  # 첫 번째 템포 값 사용
        else:
            tempo = estimated_tempo if estimated_tempo > 0 else 120  # 기본값 120 BPM

        # ✅ 박자 (Time Signature) 가져오기
        if midi_data.time_signature_changes:
            time_signature = f"{midi_data.time_signature_changes[0].numerator}/{midi_data.time_signature_changes[0].denominator}"
        else:
            time_signature = "4/4"  # 기본값 4/4

        # ✅ 키 가져오기
        if midi_data.key_signature_changes:
            key_number = midi_data.key_signature_changes[0].key_number
        else:
            key_number = 0  # 기본값 C Major

        key_map = ["C Major", "G Major", "D Major", "A Major", "E Major", "B Major", "F# Major",
                   "C# Major", "F Major", "Bb Major", "Eb Major", "Ab Major", "Db Major", "Gb Major",
                   "Cb Major", "A Minor", "E Minor", "B Minor", "F# Minor", "C# Minor", "G# Minor",
                   "D# Minor", "A# Minor", "D Minor", "G Minor", "C Minor", "F Minor", "Bb Minor",
                   "Eb Minor", "Ab Minor"]
        key = key_map[key_number] if key_number < len(key_map) else "C Major"

        chords, melody, rhythm_pattern, drum_pattern = [], [], [], []
        instruments = set()

        for instrument in midi_data.instruments:
            if instrument.is_drum:
                # ✅ 드럼 트랙의 주요 타격 피치 저장
                drum_pattern.extend([note.pitch for note in instrument.notes if note.velocity > 0])
            else:
                instruments.add(instrument.name)  # 🎺 주요 악기 저장

                # ✅ 멜로디 및 리듬 패턴 저장
                for note in instrument.notes:
                    melody.append({
                        "pitch": note.pitch,
                        "start_time": note.start,
                        "duration": note.end - note.start,
                        "velocity": note.velocity
                    })
                    rhythm_pattern.append(note.end - note.start)  # 지속 시간 기반 리듬 패턴

                # ✅ 코드 진행 추출 (각 악기에서 처음 3개 이상의 노트 조합)
                if len(instrument.notes) >= 3:
                    chord_notes = sorted(set(note.pitch for note in instrument.notes[:3]))  # 코드 구성음
                    if chord_notes not in chords:
                        chords.append(chord_notes)

        # ✅ 데이터 정제
        return {
            "genre": "jazz",
            "tempo": int(tempo),
            "time_signature": time_signature,
            "key": key,
            "chord_progression": chords[:10],  # 🎼 10개까지만 저장
            "melody": melody[:10],  # 🎵 샘플로 10개만 저장 (나중에 전부 포함 가능)
            "rhythm_pattern": rhythm_pattern[:10],  # 🎶 샘플로 10개만 저장
            "instruments": list(instruments) if instruments else ["Acoustic Grand Piano"],  # 기본 악기 설정
            "drum_pattern": list(set(drum_pattern)),  # 중복 제거
            "midi_file": os.path.basename(midi_path)
        }
        print(f"✅ 처리 완료: {midi_path}")  # 🎯 처리 완료 메시지 추가
        return extracted_features


    except Exception as e:
        print(f"⚠️ 오류 발생: {midi_path} - {e}")
        if os.path.exists(midi_path):  # ✅ 파일이 존재할 때만 삭제
            os.remove(midi_path)
            print(f"🗑️ 삭제 완료: {midi_path}")
        return None


def process_jazz():
    midi_data_list = []

    for midi_file in os.listdir(JAZZ_DIR):
        if midi_file.endswith(".mid"):
            midi_path = os.path.join(JAZZ_DIR, midi_file)
            features = extract_jazz_features(midi_path)
            if features:
                midi_data_list.append(features)
                print(f"📂 JSON 데이터 추가됨: {midi_file}")  # 🎯 JSON 데이터 추가 확인 로그

    print(f"\n🎼 총 {len(midi_data_list)}개의 MIDI 파일 처리 완료!\n")  # 🎯 전체 파일 처리 완료 로그 추가
    return midi_data_list


# ✅ JSON 파일 저장
jazz_data = {"jazz": process_jazz()}
json_path = os.path.join(SAVE_DIR, "jazz_dataset.json")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(jazz_data, f, indent=4)

print(f"✅ JSON 데이터 저장 완료: {json_path}")

# ✅ 샘플 10개 출력 코드
print("\n🎶 [샘플 JSON 데이터 10개 출력]")
for i, sample in enumerate(jazz_data["jazz"][:10]):
    print(f"\n🎼 샘플 {i + 1}:")
    print(json.dumps(sample, indent=4))

print("\n✅ 샘플 출력 완료!")