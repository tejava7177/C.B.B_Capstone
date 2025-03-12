import pretty_midi
import os
import sys

# ✅ 프로젝트 경로 설정
PROJECT_DIR = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi"
sys.path.extend([
    PROJECT_DIR,
    os.path.join(PROJECT_DIR, "punk"),
    os.path.join(PROJECT_DIR, "instruments")
])


# ✅ CHORD_TO_NOTES 가져오기
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES


# ✅ 악기별 트랙 불러오기
from drum_punk import add_punk_drum_track  # 🥁 펑크 드럼
from guitar_punk import add_punk_guitar_track  # 🎸 펑크 기타

# ✅ MIDI 저장 경로
MIDI_SAVE_PATH = os.path.join(PROJECT_DIR, "logicFiles/punk")


def generate_punk_backing_track(chord_progression, bpm=180, filename="punk_test.mid"):
    """🎸 Punk 백킹 트랙 생성 (드럼 + 기타)"""

    if not isinstance(chord_progression, list):
        raise TypeError(f"❌ 오류: chord_progression이 리스트가 아님! 현재 타입: {type(chord_progression)}")

    midi = pretty_midi.PrettyMIDI()
    start_time = 0.0
    beats_per_second = bpm / 60.0
    chord_duration = 4 / beats_per_second

    num_bars = len(chord_progression)

    # ✅ 드럼 트랙 추가
    print("🥁 Adding Punk Drum Track...")
    add_punk_drum_track(midi, start_time, chord_duration, num_bars)

    # ✅ 기타 트랙 추가
    print("🎸 Adding Punk Guitar Track...")
    add_punk_guitar_track(midi, start_time, chord_duration, chord_progression)

    output_path = os.path.join(MIDI_SAVE_PATH, filename)
    midi.write(output_path)
    print(f"✅ Punk 백킹 트랙 생성 완료: {output_path}")


# 🎵 Punk 코드 진행 샘플
punk_chords = ["C5", "G5", "F5", "E5", "G5", "E5", "G5", "A5"]

# ✅ Punk 트랙 생성 실행
generate_punk_backing_track(punk_chords, bpm=180, filename="punkBacking0312.mid")