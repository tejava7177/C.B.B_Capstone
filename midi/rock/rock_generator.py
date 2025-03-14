import pretty_midi
import os
import sys

# ✅ 프로젝트 경로 설정
PROJECT_DIR = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi"
sys.path.extend([
    PROJECT_DIR,
    os.path.join(PROJECT_DIR, "rock"),
])

# ✅ 악기별 트랙 불러오기
from drum_rock import add_rock_drum_track  # 🥁 락 드럼
# from guitar_rock import add_rock_guitar_track  # 🎸 락 기타
# from synth_rock import add_rock_synth_track  # 🎹 락 신디사이저

# ✅ MIDI 저장 경로
MIDI_SAVE_PATH = os.path.join(PROJECT_DIR, "logicFiles/rock")


def generate_rock_backing_track(chord_progression, bpm=140, filename="rock_test.mid"):
    """🎸 락 백킹 트랙 생성 (드럼 + 기타 + 신디 포함)"""

    # ✅ 코드 진행이 리스트인지 확인 (예외 처리)
    if not isinstance(chord_progression, list):
        raise TypeError(f"❌ 오류: chord_progression이 리스트가 아님! 현재 타입: {type(chord_progression)}")

    midi = pretty_midi.PrettyMIDI()
    start_time = 0.0

    # ✅ 코드 진행 1마디당 길이 계산 (4박자 기준)
    beats_per_second = bpm / 60.0
    chord_duration = 4 / beats_per_second  # 🎵 코드 지속 시간 (1마디 기준)

    # ✅ 1. 드럼 트랙 추가
    print("🥁 Adding Rock Drum Track...")
    add_rock_drum_track(midi, start_time, chord_duration, len(chord_progression))

    # # ✅ 2. 기타 트랙 추가
    # print("🎸 Adding Rock Guitar Track...")
    # add_rock_guitar_track(midi, start_time, chord_duration, chord_progression)
    #
    # # ✅ 3. 신디사이저 트랙 추가 (선택사항)
    # print("🎹 Adding Rock Synth Track...")
    # add_rock_synth_track(midi, start_time, chord_duration, chord_progression)
    #
    # ✅ MIDI 파일 저장
    output_path = os.path.join(MIDI_SAVE_PATH, filename)
    midi.write(output_path)
    print(f"✅ 락 백킹 트랙 생성 완료: {output_path}")


# 🎵 Rock 코드 진행 샘플
rock_chords = ["C5", "G5", "A5", "F5", "D5", "G5", "A5", "E5"]

# ✅ Rock 트랙 생성 실행
generate_rock_backing_track(rock_chords, bpm=140, filename="rockBacking0314.mid")