import json

# MIDI 코드 진행 데이터 로드
with open("/Users/simjuheun/Desktop/개인프로젝트/C.B.B/data/chord_melody_data.json", "r") as f:
    midi_chord_data = json.load(f)

# 코드 빈도 분석
chord_counts = {}
for entry in midi_chord_data:
    for chord in entry["chords"]:
        chord_counts[chord] = chord_counts.get(chord, 0) + 1

# 빈도순 출력
sorted_chords = sorted(chord_counts.items(), key=lambda x: x[1], reverse=True)

print("🎵 코드 빈도 분석:")
for chord, count in sorted_chords[:20]:  # 상위 20개만 출력
    print(f"{chord}: {count}회")