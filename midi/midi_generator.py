import pretty_midi
import sys
import os
import random

# ✅ 경로 설정
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/instruments")
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/scale")
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/test")
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/drum")



# ✅ 악기별 트랙 불러오기
from drums import add_drum_track
from click_track import add_click_track
from generate_melody import generate_melody_from_chords
from guitar import add_guitar_lead_track  # ✅ 기존 기타 코드 기반 트랙 추가
#from piano import add_piano_track  # ✅ 기존 피아노 코드 기반 트랙 추가

# ✅ MIDI 저장 경로
MIDI_SAVE_PATH = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/logicFiles"


def add_melody_track(midi, melody_data, start_time, total_duration, instrument_program=0):
    """🎵 멜로디 트랙 추가 (건반 or 기타 멜로디)"""

    melody = pretty_midi.Instrument(program=instrument_program)  # 기본 건반 (Acoustic Grand Piano)

    previous_note = None  # 직전 음
    min_notes_per_chord = 4  # ✅ 각 코드당 최소한의 멜로디 음 개수 보장
    max_jump = 6  # ✅ 도약 허용 범위를 6도까지 확장

    melody_buffer = []  # 멜로디 음을 미리 저장 후 추가

    for note, start, end in melody_data:
        # ✅ 멜로디 시작을 Click Track이 끝난 시점부터 맞추기
        adjusted_start = start + start_time
        adjusted_end = end + start_time

        # ✅ 멜로디가 백킹 트랙 길이보다 길어지지 않도록 조정
        if adjusted_end <= start_time + total_duration:
            # ✅ 음역 제한 (C3 ~ C6, MIDI 48~84)
            if 48 <= note <= 84:
                # ✅ 이전 음과 너무 큰 도약 방지 (6도 이상 차이 X)
                if previous_note is None or abs(previous_note - note) <= max_jump:
                    melody_buffer.append(pretty_midi.Note(
                        velocity=100, pitch=note, start=adjusted_start, end=adjusted_end
                    ))
                    previous_note = note  # 현재 음을 다음 반복문에서 참고

    # ✅ 멜로디 음 개수 조정 (최소 4개 이상)
    if len(melody_buffer) < min_notes_per_chord:
        extra_notes = random.choices(melody_buffer, k=min_notes_per_chord - len(melody_buffer))
        melody_buffer.extend(extra_notes)  # 부족한 만큼 추가

    melody.notes.extend(melody_buffer)
    midi.instruments.append(melody)


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

    # ✅ 3. 멜로디 생성 (기본 코드 진행 기반)
    melody_data = generate_melody_from_chords(chord_progression)

    # ✅ 4. 기존 백킹 트랙 추가 (Click Track 이후)
    #add_piano_track(midi, chord_progression, start_time, chord_duration)
    add_drum_track(midi, start_time, chord_duration, chord_progression)
    add_guitar_lead_track(midi, chord_progression, start_time, chord_duration)

    # ✅ 5. 멜로디 추가 (Click Track 이후, 백킹 트랙 길이 맞춤)
    add_melody_track(midi, melody_data, start_time, total_duration)

    # ✅ 6. MIDI 파일 저장
    output_path = os.path.join(MIDI_SAVE_PATH, filename)
    midi.write(output_path)
    print(f"✅ 멜로디 포함 MIDI 파일 생성 완료: {output_path}")


# 🎵 AI가 생성한 코드 진행
ai_generated_chords = ["Gmaj7", "Am7", "Bm7", "Em7", "Bsus4", "E Major", "C Major" , "B Major", "Emaj7" , "Amaj7"]

# ✅ MIDI 파일 생성 실행
save_melody_to_midi(ai_generated_chords, bpm=120, filename="melody_test.mid")