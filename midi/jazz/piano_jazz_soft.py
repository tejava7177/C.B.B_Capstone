import pretty_midi
import random
import sys

# ✅ CHORD_TO_NOTES 가져오기
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES

# 🎹 부드러운 코드 보이싱
SOFT_JAZZ_VOICINGS = {
    "Cmaj7": [60, 64, 67, 71],
    "Dm7": [62, 65, 69, 72],
    "G7": [43, 50, 53, 57],
    "Fmaj7": [41, 45, 48, 52],
    "Bm7": [47, 50, 54, 57],
    "E7": [40, 47, 50, 54],
    "Am7": [45, 48, 52, 55]
}

# 🎵 부드러운 리듬 패턴
SOFT_RHYTHM_PATTERNS = [
    [0],  # 첫 박자에서 코드 연주 후 유지
    [0, 1.5, 3],  # 첫 박자, 엇박에서 연주
    [0, 2, 3.5],  # 첫 박자, 셋째 박자 반 박자 뒤에서 연주
]


def get_soft_jazz_voicing(chord):
    """🎵 코드에 따른 부드러운 재즈 보이싱 생성"""

    # ✅ 리스트인지 확인 후 문자열 코드 이름을 유지
    if isinstance(chord, list):
        print(f"⚠️ Warning: 코드가 리스트로 전달됨: {chord}. 첫 번째 코드 사용.")
        chord = chord[0]  # 첫 번째 코드만 사용

    # ✅ 문자열 코드인지 확인 (숫자가 아니라면 정상적으로 변환됨)
    if isinstance(chord, str):
        if chord in CHORD_TO_NOTES:
            return CHORD_TO_NOTES[chord]  # 정상 코드 반환
        else:
            print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 없음. 기본 Cmaj7 사용")
            return SOFT_JAZZ_VOICINGS["Cmaj7"]

    # ⚠️ 숫자 리스트로 변환된 경우, 강제로 기본 Cmaj7 사용 (예외 방지)
    print(f"⚠️ Warning: '{chord}' 잘못된 코드 형식 감지. 기본 Cmaj7 사용.")
    return SOFT_JAZZ_VOICINGS["Cmaj7"]


def add_soft_jazz_piano_track(midi, start_time, duration, chord_progression):
    """🎹 부드러운 재즈 피아노 코드 컴핑"""

    piano = pretty_midi.Instrument(program=0)  # 🎹 Acoustic Grand Piano

    for bar, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar * duration)
        chord_notes = get_soft_jazz_voicing(chord)  # ✅ 수정된 코드 보이싱 함수 사용

        # ✅ 랜덤한 부드러운 리듬 패턴 선택
        rhythm_pattern = random.choice(SOFT_RHYTHM_PATTERNS)

        # ✅ 왼손 (루트음)과 오른손 (보이싱) 분리
        left_hand = [chord_notes[0] - 12]  # 루트 노트 (옥타브 낮춤)
        right_hand = chord_notes[1:]  # 나머지 보이싱

        for beat in rhythm_pattern:
            beat_time = bar_start_time + (beat * (duration / 4))
            beat_time += random.uniform(-0.05, 0.05)  # 🎵 박자 랜덤 딜레이

            # 🎹 왼손 (루트음) 추가 - 부드럽게 연결
            for note in left_hand:
                piano.notes.append(pretty_midi.Note(
                    velocity=random.randint(70, 85),
                    pitch=note,
                    start=beat_time,
                    end=beat_time + duration * 0.9  # 90% 유지
                ))

            # 🎹 오른손 (코드 보이싱) 추가 - 자연스럽게 유지
            for note in right_hand:
                piano.notes.append(pretty_midi.Note(
                    velocity=random.randint(75, 95),
                    pitch=note,
                    start=beat_time + random.uniform(0.02, 0.08),  # 🎵 시간차 적용
                    end=beat_time + duration * 0.75  # 75% 유지
                ))

    midi.instruments.append(piano)