import pretty_midi

def analyze_midi(file_path):
    """주어진 MIDI 파일을 분석하여 트랙, 노트 개수, 리듬 패턴을 출력하는 함수"""
    try:
        midi_data = pretty_midi.PrettyMIDI(file_path)
        print(f"✅ MIDI 파일 로드 완료: {file_path}\n")

        # 🎼 전체 트랙 정보 출력
        print("🎵 [ 트랙(Instrument) 정보 ]")
        for i, instrument in enumerate(midi_data.instruments):
            instrument_name = pretty_midi.program_to_instrument_name(instrument.program)
            instrument_type = "Drum" if instrument.is_drum else "Melodic"
            print(f"  🎹 트랙 {i + 1}: {instrument_name} ({instrument_type}) - 노트 개수: {len(instrument.notes)}")

        print("\n🎶 [ 개별 트랙 노트 정보 ]")
        for i, instrument in enumerate(midi_data.instruments):
            print(f"\n🎼 트랙 {i + 1}: {pretty_midi.program_to_instrument_name(instrument.program)}")
            print("   시작시간 | 종료시간 | 피치 | 속도")
            print("   ---------------------------------")
            for note in instrument.notes[:10]:  # 처음 10개 노트만 출력
                print(f"   {note.start:.2f} | {note.end:.2f} | {note.pitch} | {note.velocity}")

        # 🥁 드럼 패턴 확인
        drum_tracks = [inst for inst in midi_data.instruments if inst.is_drum]
        if drum_tracks:
            print("\n🥁 [ 드럼 패턴 ]")
            for i, drum in enumerate(drum_tracks):
                print(f"  🥁 트랙 {i + 1} - 노트 개수: {len(drum.notes)}")
                unique_drums = set(note.pitch for note in drum.notes)
                print(f"  사용된 드럼 종류 (피치): {sorted(unique_drums)}")

        print("\n🎼 MIDI 분석 완료!")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

# 📌 분석할 MIDI 파일 경로
midi_file_path ="/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/generated_jazz.mid"

# 🧐 MIDI 파일 분석 실행
analyze_midi(midi_file_path)