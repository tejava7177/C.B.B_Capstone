import pretty_midi
import random

def get_melody_range_for_chord(chord):
    """🎵 코드에 따라 멜로디 음역대 설정 (자연스러운 진행)"""
    if "Cmaj" in chord or "Gmaj" in chord or "Fmaj" in chord:
        return (48, 72)  # C3 ~ C5
    elif "Dmin" in chord or "Emin" in chord:
        return (50, 74)  # D3 ~ D5
    elif "Bdim" in chord or "G7" in chord:
        return (47, 71)  # B3 ~ G5
    return (48, 72)  # 기본값

def generate_melody_from_chords(chord_progression):
    """🎵 코드 기반으로 멜로디 생성 (코드에 맞춘 음역대 조정 + 변주 추가)"""
    melody_notes = []
    start_time = 0.0
    note_duration = 0.5  # 기본 한 음 길이 (4분음표)

    for chord in chord_progression:
        # ✅ 코드에 맞는 음역대 적용
        min_pitch, max_pitch = get_melody_range_for_chord(chord)

        # ✅ 멜로디 변주 추가
        num_notes = random.randint(2, 4)  # 한 마디에 최소 2~4개 음 추가
        notes_in_bar = []

        for _ in range(num_notes):
            note_pitch = random.randint(min_pitch, max_pitch)
            notes_in_bar.append((note_pitch, start_time, start_time + note_duration))
            start_time += note_duration  # 다음 음 시간 갱신

        melody_notes.extend(notes_in_bar)

    return melody_notes  # ✅ 생성된 멜로디 데이터 반환

def add_melody_track(midi, chord_progression, start_time, total_duration, instrument_program=0):
    """🎵 건반 멜로디 트랙 추가 (자연스러운 변주 및 리듬감 적용)"""

    melody = pretty_midi.Instrument(program=0)  # 기본 건반 (Acoustic Grand Piano)

    # ✅ 새로운 멜로디 생성 방식 적용
    melody_data = generate_melody_from_chords(chord_progression)

    for i, (note, start, end) in enumerate(melody_data):
        adjusted_start = start + start_time
        adjusted_end = end + start_time

        # ✅ 멜로디가 백킹 트랙 길이를 넘지 않도록 조정
        if adjusted_end <= start_time + total_duration:
            # ✅ Velocity (강약 조절) 적용
            velocity = 100 if i % 4 == 0 else (80 if i % 4 == 2 else 90)

            melody.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=note, start=adjusted_start, end=adjusted_end
            ))

    midi.instruments.append(melody)