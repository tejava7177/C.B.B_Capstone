import pretty_midi
import random
import sys

# ✅ CHORD_TO_NOTES 가져오기 (Jazz에서 사용한 방식)
sys.path.append("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord")
from chord_to_notes import CHORD_TO_NOTES

# ✅ 신디사이저 패드 프로그램 번호 (GM MIDI 기준)
SYNTH_PAD_PROGRAM = 89  # Pad 5 (Bowed)

def add_punk_synth_track(midi, start_time, duration, chord_progression):
    """🎹 펑크 신디사이저 트랙 추가 (배경 패드 느낌)"""

    synth_pad = pretty_midi.Instrument(program=SYNTH_PAD_PROGRAM)  # 🎹 신디사이저 패드

    for bar, chord in enumerate(chord_progression):
        bar_start_time = start_time + (bar * duration)

        # 코드에 해당하는 MIDI 노트 가져오기
        if chord in CHORD_TO_NOTES:
            chord_notes = CHORD_TO_NOTES[chord]
        else:
            print(f"⚠️ Warning: '{chord}' 코드가 CHORD_TO_NOTES에 없음. 기본 C Major 사용")
            chord_notes = CHORD_TO_NOTES["C Major"]

        # ✅ 신디 패드: 코드 전체를 부드럽게 유지 (배경용)
        for note in chord_notes:
            synth_pad.notes.append(pretty_midi.Note(
                velocity=random.randint(50, 70),  # 약간 낮은 볼륨으로 배경화
                pitch=note,
                start=bar_start_time,
                end=bar_start_time + duration * 0.95  # 거의 한 마디 지속
            ))

        # ✅ 약간의 리듬감을 주기 위해 8비트 패턴 추가 (랜덤)
        if random.random() > 0.7:
            beat_time = bar_start_time + (duration / 2)
            for note in chord_notes:
                synth_pad.notes.append(pretty_midi.Note(
                    velocity=random.randint(40, 60),
                    pitch=note,
                    start=beat_time,
                    end=beat_time + duration * 0.4  # 짧게 울림
                ))

    midi.instruments.append(synth_pad)