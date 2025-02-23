import pretty_midi
import sys
import os
import random

# 🛠️ `chord_to_notes.py` 경로 추가
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")

# CHORD_TO_NOTES 가져오기
from chord_to_notes import CHORD_TO_NOTES

# 🎯 MIDI 파일 저장 경로 설정
MIDI_SAVE_PATH = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/midi/midiFiles_logic"


# 🥁 4박자 내내 연주되는 드럼 패턴
def add_full_beat_drum_pattern(drum, start_time, duration):
    """4박자를 꽉 채운 드럼 패턴 추가"""

    # 드럼 음표 정의 (General MIDI Percussion)
    kick_drum = 36  # Bass Drum
    snare_drum = 38  # Snare Drum
    closed_hihat = 42
    open_hihat = 46
    crash_cymbal = 49
    ride_cymbal = 51
    tom1 = 48  # High Tom
    tom2 = 45  # Low Tom

    # 기본적인 4박자 리듬
    for i in range(4):
        beat_time = start_time + (i * (duration / 4))

        # 킥 드럼 (1박, 3박 강하게)
        if i % 2 == 0:
            drum.notes.append(pretty_midi.Note(velocity=random.randint(90, 120), pitch=kick_drum, start=beat_time,
                                               end=beat_time + 0.1))

        # 스네어 드럼 (2박, 4박)
        if i % 2 == 1:
            drum.notes.append(pretty_midi.Note(velocity=random.randint(90, 120), pitch=snare_drum, start=beat_time,
                                               end=beat_time + 0.1))

        # 하이햇 (4박자 내내 추가)
        if random.random() > 0.7:
            drum.notes.append(pretty_midi.Note(velocity=80, pitch=open_hihat, start=beat_time, end=beat_time + 0.1))
        else:
            drum.notes.append(pretty_midi.Note(velocity=80, pitch=closed_hihat, start=beat_time, end=beat_time + 0.1))

    # 8마디마다 심벌 & 탐탐 필 추가
    if int(start_time) % 8 == 0:
        drum.notes.append(pretty_midi.Note(velocity=100, pitch=crash_cymbal, start=start_time, end=start_time + 0.5))
        drum.notes.append(pretty_midi.Note(velocity=90, pitch=tom1, start=start_time + 0.6, end=start_time + 0.7))
        drum.notes.append(pretty_midi.Note(velocity=90, pitch=tom2, start=start_time + 0.7, end=start_time + 0.8))


def save_chord_progression_to_midi(chord_progression, bpm=120, filename="output.mid"):
    """AI가 생성한 코드 진행을 MIDI 파일로 변환하고 4박자 드럼 추가"""

    midi = pretty_midi.PrettyMIDI()

    # 🎹 건반(피아노) 트랙 추가
    piano = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    # 🥁 드럼 트랙 추가 (MIDI 채널 10)
    drum = pretty_midi.Instrument(program=0, is_drum=True)

    start_time = 0.0
    beats_per_second = bpm / 60.0  # BPM을 초 단위로 변환
    chord_duration = 4 / beats_per_second  # 4박자 지속 시간

    for chord in chord_progression:
        # 🔹 코드 진행 추가 (피아노 트랙)
        midi_notes = CHORD_TO_NOTES.get(chord, [60, 64, 67])  # 기본값: C Major

        for note_number in midi_notes:
            note = pretty_midi.Note(
                velocity=100, pitch=note_number, start=start_time, end=start_time + chord_duration
            )
            piano.notes.append(note)

        # 🥁 4박자 드럼 패턴 추가
        add_full_beat_drum_pattern(drum, start_time, chord_duration)

        start_time += chord_duration  # 다음 코드로 진행

    midi.instruments.append(piano)
    midi.instruments.append(drum)  # 🎵 드럼 트랙 추가

    # 🎯 지정된 경로에 MIDI 파일 저장
    output_path = os.path.join(MIDI_SAVE_PATH, filename)
    midi.write(output_path)
    print(f"✅ MIDI 파일이 생성되었습니다: {output_path}")


# 🎵 AI가 생성한 코드 진행 (샘플)
ai_generated_chords = ["C9", "G9", "F9", "E7", "G9", "E Major", "G9", "Amaj7",
                       "Cmaj7", "Bsus4", "Dmaj7", "D9", "Amaj7", "Dmaj7", "B7"]

# MIDI 파일 생성 (4박자 적용)
save_chord_progression_to_midi(ai_generated_chords, bpm=120, filename="ai_generated_chords_full_drums.mid")