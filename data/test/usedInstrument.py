import pretty_midi

def list_instruments(midi_file):
    """MIDI 파일에서 사용된 악기 목록을 출력"""
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    print(f"🎵 사용된 악기 목록 ({midi_file}):\n")

    for idx, instrument in enumerate(midi_data.instruments):
        # 프로그램 번호를 악기 이름으로 변환
        instrument_name = pretty_midi.program_to_instrument_name(instrument.program)
        is_drum = "🛢 Drum Track" if instrument.is_drum else ""
        note_count = len(instrument.notes)  # 사용된 노트 개수

        print(f"🎹 Instrument {idx+1}: {instrument_name} (Program: {instrument.program}) {is_drum}")
        print(f"   🎼 사용된 노트 개수: {note_count}\n")

# MIDI 파일 경로
midi_file_path = '/Volumes/Extreme SSD/lmd_aligned/O/C/D/TROCDKD128F92F128F/d52962c211dfebeffe92117855cffd3b.mid'

# 사용된 악기 목록 출력
list_instruments(midi_file_path)