import pretty_midi
import os
import sys

# ✅ 경로 설정
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi")
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/jazz")
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/instruments")

# ✅ 악기별 트랙 불러오기
from drums_jazz import add_jazz_drum_track  # 🎷 재즈 드럼
from guitar_jazz import add_jazz_guitar_comping  # 🎸 코드 컴핑
from piano_jazz import add_jazz_piano_track  # 🎹 재즈 피아노

# ✅ MIDI 저장 경로
MIDI_SAVE_PATH = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/logicFiles/jazz"

def generate_jazz_backing_track(chord_progression, bpm=120, filename="jazz_test.mid"):
    """🎷 재즈 백킹 트랙 생성 (드럼 + 기타 + 피아노 포함)"""
    if not isinstance(chord_progression, list):
        raise TypeError(f"❌ 오류: chord_progression이 리스트가 아님! 현재 타입: {type(chord_progression)}")

    midi = pretty_midi.PrettyMIDI()
    start_time = 0.0

    # ✅ 코드 진행 1마디당 길이 계산 (4박자 기준)
    beats_per_second = bpm / 60.0
    chord_duration = 4 / beats_per_second  # 🎵 코드 지속 시간 (1마디 기준)

    # ✅ 1. 드럼 트랙 추가
    print("🥁 Adding Jazz Drum Track...")
    add_jazz_drum_track(midi, start_time, chord_duration, chord_progression)

    # ✅ 2. 기타 트랙 추가
    print("🎸 Adding Jazz Guitar Track...")
    add_jazz_guitar_comping(midi, start_time, chord_duration, chord_progression)  # 🎸 코드 컴핑

    # ✅ 3. 피아노 트랙 추가
    print("🎹 Adding Piano Track...")
    add_jazz_piano_track(midi, start_time, chord_duration, chord_progression)  # 🎵 인자 순서 맞춤

    # ✅ MIDI 파일 저장
    output_path = os.path.join(MIDI_SAVE_PATH, filename)
    midi.write(output_path)
    print(f"✅ 재즈 백킹 트랙 생성 완료: {output_path}")

# 🎵 Jazz 코드 진행 샘플
jazz_chords = ["Cmaj7", "Dm7", "G7", "Cmaj7", "Fmaj7", "Bm7", "E7", "Am7"]

# ✅ Jazz 트랙 생성 실행
generate_jazz_backing_track(jazz_chords, bpm=120, filename="jazz_test.mid")