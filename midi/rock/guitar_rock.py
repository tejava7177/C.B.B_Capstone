import pretty_midi
import random
from typing import List
import sys
# 🎸 락 기타 MIDI 프로그램 번호 (Distortion Guitar)
DISTORTION_GUITAR = 30

# 휴먼라이제이션을 위한 파라미터들
TIMING_JITTER = 0.05         # 노트 시작 시간에 ±50ms 범위의 랜덤 지터
DURATION_VARIATION = 0.05     # 노트 길이에 ±50ms 범위의 변동
VELOCITY_BASE = 100          # 기본 벨로시티
VELOCITY_VARIATION = 10      # 벨로시티 변동 범위

# 🎵 락 리프 패턴 (Riffs)
ROCK_RIFF_PATTERNS = [
    [0, 2, 3, 5, 3, 2],      # 기본 리프
    [0, 3, 5, 7, 5, 3],      # 확장 리프
    [0, 5, 7, 9, 7, 5, 3, 2]  # 롱 리프
]

# ✅ CHORD_TO_NOTES 가져오기
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES

def get_guitar_chord_notes(chord: str) -> List[int]:
    """
    주어진 코드에 해당하는 기타 노트를 반환합니다.
    만약 코드가 CHORD_TO_NOTES에 없으면 기본값 C5의 노트를 사용합니다.
    """
    if chord in CHORD_TO_NOTES:
        return CHORD_TO_NOTES[chord]
    else:
        print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 없음. 기본 C5 사용")
        return CHORD_TO_NOTES["C5"]

def add_rock_guitar_track(midi: pretty_midi.PrettyMIDI, start_time: float, duration: float, chord_progression: List[str]) -> None:
    """
    주어진 MIDI 객체에 락 기타 트랙을 추가합니다.
    코드 진행에 맞춰 다운스트로크와 8마디마다 리프를 추가하며,
    타이밍, 벨로시티, 노트 길이에 랜덤 변동을 적용하여 자연스러운 연주감을 모방합니다.
    """
    guitar = pretty_midi.Instrument(program=DISTORTION_GUITAR)

    for bar_index, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar_index * duration)
        chord_notes = get_guitar_chord_notes(chord)

        # 각 마디에서 4분음표 다운스트로크 적용
        for beat in range(4):
            # 기본 박자 시간 계산 후 랜덤 지터 추가
            beat_time = bar_start_time + beat * (duration / 4) + random.uniform(-TIMING_JITTER, TIMING_JITTER)
            # 벨로시티를 기본 값에서 랜덤 변동 적용
            velocity = VELOCITY_BASE + random.randint(-VELOCITY_VARIATION, VELOCITY_VARIATION)
            # 노트 지속 시간도 약간 변동
            note_duration = (duration / 4) * 0.75 + random.uniform(-DURATION_VARIATION, DURATION_VARIATION)

            for note in chord_notes:
                guitar.notes.append(pretty_midi.Note(
                    velocity=velocity,
                    pitch=note,
                    start=beat_time,
                    end=beat_time + note_duration
                ))

        # 8마디마다 리프 추가 (마디 번호는 0부터 시작하므로 bar_index+1 % 8 == 0)
        if (bar_index + 1) % 8 == 0:
            riff_pattern = random.choice(ROCK_RIFF_PATTERNS)
            # 리프 시작 시간은 해당 마디의 마지막 박자에서 시작
            riff_start_time = bar_start_time + 3 * (duration / 4) + random.uniform(-TIMING_JITTER, TIMING_JITTER)
            for i, interval in enumerate(riff_pattern):
                riff_note_time = riff_start_time + i * 0.1 + random.uniform(-TIMING_JITTER, TIMING_JITTER)
                riff_velocity = VELOCITY_BASE + random.randint(-VELOCITY_VARIATION, VELOCITY_VARIATION)
                riff_note_duration = 0.2 + random.uniform(-DURATION_VARIATION, DURATION_VARIATION)
                # 루트 음에서 간격(interval)을 더해 리프 노트 결정
                riff_note = chord_notes[0] + interval
                guitar.notes.append(pretty_midi.Note(
                    velocity=riff_velocity,
                    pitch=riff_note,
                    start=riff_note_time,
                    end=riff_note_time + riff_note_duration
                ))

    midi.instruments.append(guitar)