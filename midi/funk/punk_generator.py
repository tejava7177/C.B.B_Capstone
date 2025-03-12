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

# ✅ 악기별 트랙 불러오기
from drum_punk import add_punk_drum_track  # 🥁 펑크 드럼

# from punk_guitar import add_punk_guitar_track  # 🎸 펑크 기타 (추후 활성화)
# from punk_bass import add_punk_bass_track  # 🎸 펑크 베이스 (추후 활성화)
# from punk_synth import add_punk_synth_track  # 🎹 펑크 신디사이저 (선택사항)

# ✅ MIDI 저장 경로
MIDI_SAVE_PATH = os.path.join(PROJECT_DIR, "logicFiles/punk")


def generate_punk_backing_track(chord_progression, bpm=180, filename="punk_test.mid"):
    """🎸 펑크 백킹 트랙 생성 (드럼 + 기타 + 베이스 + 신디 포함)"""

    # ✅ 코드 진행이 리스트인지 확인 (예외 처리)
    if not isinstance(chord_progression, list):
        raise TypeError(f"❌ 오류: chord_progression이 리스트가 아님! 현재 타입: {type(chord_progression)}")

    midi = pretty_midi.PrettyMIDI()
    start_time = 0.0

    # ✅ 코드 진행 1마디당 길이 계산 (4박자 기준)
    beats_per_second = bpm / 60.0
    chord_duration = 4 / beats_per_second  # 🎵 코드 지속 시간 (1마디 기준)

    # ✅ 코드 진행 개수에 맞춰 마디 수 계산
    num_bars = len(chord_progression)

    # ✅ 1. 드럼 트랙 추가
    print("🥁 Adding Punk Drum Track...")
    add_punk_drum_track(midi, start_time, chord_duration, num_bars)

    # # ✅ 2. 기타 트랙 추가 (추후 활성화)
    # print("🎸 Adding Punk Guitar Track...")
    # add_punk_guitar_track(midi, start_time, chord_duration, chord_progression)

    # # ✅ 3. 베이스 트랙 추가 (추후 활성화)
    # print("🎸 Adding Punk Bass Track...")
    # add_punk_bass_track(midi, start_time, chord_duration, chord_progression)

    # # ✅ 4. 신디사이저 트랙 추가 (선택사항, 추후 활성화)
    # print("🎹 Adding Punk Synth Track...")
    # add_punk_synth_track(midi, start_time, chord_duration, chord_progression)

    # ✅ MIDI 파일 저장
    output_path = os.path.join(MIDI_SAVE_PATH, filename)
    midi.write(output_path)
    print(f"✅ 펑크 백킹 트랙 생성 완료: {output_path}")


# 🎵 Punk 코드 진행 샘플
punk_chords = ["A5", "D5", "E5", "A5", "G5", "C5", "F5", "G5"]

# ✅ Punk 트랙 생성 실행
generate_punk_backing_track(punk_chords, bpm=180, filename="punkBacking0312.mid")