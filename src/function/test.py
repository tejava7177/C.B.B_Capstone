import pretty_midi

# 새로운 MIDI 객체 생성
midi = pretty_midi.PrettyMIDI()

# 피아노 악기 추가
piano = pretty_midi.Instrument(program=0)

# C4, D4, E4 노트 추가
for pitch, start_time in zip([60, 62, 64], [0, 1, 2]):  # C4, D4, E4
    note = pretty_midi.Note(velocity=100, pitch=pitch, start=start_time, end=start_time + 1)
    piano.notes.append(note)

# 악기를 MIDI 객체에 추가
midi.instruments.append(piano)

# MIDI 파일 저장
midi.write('output.mid')
print("MIDI 파일이 생성되었습니다: output.mid")