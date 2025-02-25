import pretty_midi
import sys
import os

# ✅ instruments 폴더 경로 추가
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/instruments")

# ✅ 각 악기별 트랙 추가 함수 불러오기
from piano import add_piano_track
from drums import add_drum_track
from guitar import add_guitar_track

# ✅ MIDI 파일 저장 경로
MIDI_SAVE_PATH = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/logicFiles"

def save_chord_progression_to_midi(chord_progression, bpm=120, filename="basic_backingTrack.mid"):
    """AI가 생성한 코드 진행을 MIDI 파일로 변환하고 기본 백킹 트랙 추가"""

    midi = pretty_midi.PrettyMIDI()
    start_time = 0.0
    beats_per_second = bpm / 60.0  # BPM을 초 단위로 변환
    chord_duration = 4 / beats_per_second  # 4박자 지속 시간

    # 🎹 피아노 트랙 추가
    add_piano_track(midi, chord_progression, start_time, chord_duration)

    # 🥁 드럼 트랙 추가
    add_drum_track(midi, start_time, chord_duration, chord_progression)

    # 🎸 기타 트랙 추가 (✅ 기본적으로 항상 포함)
    add_guitar_track(midi, chord_progression, start_time, chord_duration)

    # 🎯 지정된 경로에 MIDI 파일 저장
    output_path = os.path.join(MIDI_SAVE_PATH, filename)
    midi.write(output_path)
    print(f"✅ 기본 백킹 트랙 MIDI 파일이 생성되었습니다: {output_path}")

# 🎵 AI가 생성한 코드 진행 (샘플)
ai_generated_chords = ["C9", "G9", "F9", "E7", "G9", "E Major", "G9", "Amaj7",
                       "Cmaj7", "Bsus4", "Dmaj7", "D9", "Amaj7", "Dmaj7", "B7"]

# ✅ 기본 백킹 트랙 MIDI 생성 (건반 + 드럼 + 기타 포함)
save_chord_progression_to_midi(ai_generated_chords, bpm=120)