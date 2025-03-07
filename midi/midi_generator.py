import pretty_midi
import sys
import os
import random

# ✅ 경로 설정
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/instruments")
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/scale")
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/test")

# ✅ 악기별 트랙 불러오기
from drums import add_drum_track
from click_track import add_click_track
from guitar import add_guitar_backing_track
#from melody import add_melody_track, generate_melody_from_chords  # ✅ 멜로디 생성 함수 추가
# from piano import add_piano_track  # ✅ 기존 피아노 코드 기반 트랙 추가 가능

# ✅ MIDI 저장 경로
MIDI_SAVE_PATH = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/logicFiles"


def save_melody_to_midi(chord_progression, bpm=120, filename="melody_test.mid"):
    """🎼 멜로디를 포함한 MIDI 파일 저장"""
    midi = pretty_midi.PrettyMIDI()
    start_time = 0.0

    # ✅ 1. Click Track (틱 틱 틱 틱) 도입부 추가
    start_time = add_click_track(midi, start_time=start_time, bpm=bpm)  # 🎯 start_time 명시적으로 전달

    # ✅ 2. 백킹 트랙 길이 계산 (코드 개수 × 4박자)
    beats_per_second = bpm / 60.0
    chord_duration = 4 / beats_per_second
    total_duration = len(chord_progression) * chord_duration  # ✅ 전체 백킹 트랙 길이



    # ✅ 4. 기존 백킹 트랙 추가 (Click Track 이후)
    # add_piano_track(midi, chord_progression, start_time, chord_duration)
    add_drum_track(midi, start_time, chord_duration, chord_progression)
    add_guitar_backing_track(midi, chord_progression, start_time, chord_duration)


    # ✅ 6. MIDI 파일 저장
    output_path = os.path.join(MIDI_SAVE_PATH, filename)
    midi.write(output_path)
    print(f"✅ 멜로디 포함 MIDI 파일 생성 완료: {output_path}")


# 🎵 AI가 생성한 코드 진행
ai_generated_chords = ["Gmaj7", "Am7", "Bm7", "Em7", "D Major", "Bmaj7", "B Major", "F Major", "A Major", "Esus4"]

# ✅ MIDI 파일 생성 실행
save_melody_to_midi(ai_generated_chords, bpm=120, filename="melody_test.mid")