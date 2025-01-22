import pretty_midi

# MIDI 파일 로드
midi_data = pretty_midi.PrettyMIDI(
    '/Volumes/Extreme SSD/lmd_aligned/O/C/D/TROCDKD128F92F128F/d52962c211dfebeffe92117855cffd3b.mid')


# 악기 이름 매핑 함수
def program_to_instrument_name(program_number):
    """MIDI 프로그램 번호를 악기 이름으로 변환"""
    return pretty_midi.program_to_instrument_name(program_number)



# 노트 정보 출력
for instrument in midi_data.instruments:
    # 악기 이름 출력
    instrument_name = program_to_instrument_name(instrument.program)
    print(f"Instrument: {instrument_name} (Program: {instrument.program})")

    # 노트 정보 출력
    for note in instrument.notes:
        note_name = pretty_midi.note_number_to_name(note.pitch)
        print(f"Note: {note_name}, Start: {note.start:.2f}, End: {note.end:.2f}, Duration: {note.end - note.start:.2f}")
