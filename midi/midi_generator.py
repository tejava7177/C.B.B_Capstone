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


def add_melody_track(midi, melody_data, start_time, total_duration):
    """🎵 멜로디 트랙 추가 (건반 기본)"""
    melody = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    for note, start, end in melody_data:
        # ✅ 멜로디 시작을 Click Track이 끝난 시점부터 맞추기
        adjusted_start = start + start_time
        adjusted_end = end + start_time

        # ✅ 멜로디가 백킹 트랙 길이보다 길어지지 않도록 조정
        if adjusted_end <= start_time + total_duration:
            melody.notes.append(pretty_midi.Note(velocity=100, pitch=note, start=adjusted_start, end=adjusted_end))

    midi.instruments.append(melody)


def save_melody_to_midi(chord_progression, bpm=120, filename="melody_test.mid"):
    """🎼 멜로디를 포함한 MIDI 파일 저장"""
    midi = pretty_midi.PrettyMIDI()
    start_time = 0.0

    # ✅ 1. Click Track (틱 틱 틱 틱) 도입부 추가
    start_time = add_click_track(midi, start_time, bpm=bpm)

    # ✅ 2. 백킹 트랙 길이 계산 (코드 개수 × 4박자)
    beats_per_second = bpm / 60.0
    chord_duration = 4 / beats_per_second
    total_duration = len(chord_progression) * chord_duration  # ✅ 전체 백킹 트랙 길이

    # ✅ 3. 멜로디 생성 (기본 코드 진행 기반)
    melody_data = generate_melody_from_chords(chord_progression)

    # ✅ 4. 기존 백킹 트랙 추가 (Click Track 이후)
    add_piano_track(midi, chord_progression, start_time, chord_duration)
    add_drum_track(midi, start_time, chord_duration, chord_progression, bpm)
    add_guitar_track(midi, chord_progression, start_time, chord_duration)

    # ✅ 5. 멜로디 추가 (Click Track 이후, 백킹 트랙 길이 맞춤)
    add_melody_track(midi, melody_data, start_time, total_duration)

    # ✅ 6. MIDI 파일 저장
    output_path = os.path.join(MIDI_SAVE_PATH, filename)
    midi.write(output_path)
    print(f"✅ 멜로디 포함 MIDI 파일 생성 완료: {output_path}")


# 🎵 AI가 생성한 코드 진행
ai_generated_chords = ["C Major", "G Major", "F Minor", "C Major", "Dmaj7", "G Major", "F Major"]

# ✅ MIDI 파일 생성 실행
save_melody_to_midi(ai_generated_chords, bpm=120, filename="melody_test.mid")