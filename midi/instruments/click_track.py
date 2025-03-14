import pretty_midi

def add_click_track(midi, start_time, bpm=120):
    """✅ 독립적인 Click Track 추가 (틱 틱 틱 틱)"""
    click_track = pretty_midi.Instrument(program=0, is_drum=True)

    closed_hihat = 42  # Hi-Hat 닫힘 사운드
    click_duration = 60 / bpm  # 한 박자의 길이

    for i in range(4):  # 4박자 Click Track
        tick_time = start_time + (i * click_duration)
        click_track.notes.append(pretty_midi.Note(
            velocity=100, pitch=closed_hihat, start=tick_time, end=tick_time + 0.1
        ))

    midi.instruments.append(click_track)

    # ✅ Click Track 이후의 시작 시간 반환
    return start_time + (4 * click_duration)