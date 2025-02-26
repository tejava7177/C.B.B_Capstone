import pretty_midi
import sys
import os

# ✅ 경로 설정
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/instruments")
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/scale")
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/test")

# ✅ 악기별 트랙 불러오기
from piano import add_piano_track
from drums import add_drum_track
from guitar import add_guitar_track
from click_track import add_click_track
from generate_melody import generate_melody_from_chords

# ✅ MIDI 저장 경로
MIDI_SAVE_PATH = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/logicFiles"


def add_melody_track(midi, melody_data):
    """🎵 멜로디 트랙 추가 (건반 기본)"""
    melody = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    for note, start, end in melody_data:
        melody.notes.append(pretty_midi.Note(velocity=100, pitch=note, start=start, end=end))

    midi.instruments.append(melody)


def save_melody_to_midi(chord_progression, bpm=120, filename="melody_test.mid"):
    """🎼 멜로디를 포함한 MIDI 파일 저장"""
    midi = pretty_midi.PrettyMIDI()
    start_time = 0.0

    # ✅ 1. Click Track (틱 틱 틱 틱) 도입부 추가
    start_time = add_click_track(midi, start_time, bpm=bpm)

    # ✅ 2. 멜로디 생성 (기본 코드 진행 기반)
    melody_data = generate_melody_from_chords(chord_progression)

    # ✅ 3. 기존 백킹 트랙 추가 (Click Track 이후)
    add_piano_track(midi, chord_progression, start_time, 4)
    add_drum_track(midi, start_time, 4, chord_progression, bpm)
    add_guitar_track(midi, chord_progression, start_time, 4)

    # ✅ 4. 멜로디 추가
    add_melody_track(midi, melody_data)

    # ✅ 5. MIDI 파일 저장
    output_path = os.path.join(MIDI_SAVE_PATH, filename)
    midi.write(output_path)
    print(f"✅ 멜로디 포함 MIDI 파일 생성 완료: {output_path}")


# 🎵 AI가 생성한 코드 진행
ai_generated_chords = ["C Major", "G Major", "F Major", "E7", "A7", "D7", "G7"]

# ✅ MIDI 파일 생성 실행
save_melody_to_midi(ai_generated_chords, bpm=120, filename="melody_test.mid")