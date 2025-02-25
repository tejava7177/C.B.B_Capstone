import random
from data.scale.scale_map import get_scale_for_chord  # ✅ scale_map.py에서 스케일 불러오기

def generate_melody_from_chords(chord_progression):
    """코드 진행을 기반으로 랜덤 멜로디 생성 (더 자연스럽게 개선)"""
    melody = []
    start_time = 0.0
    previous_note = None  # 이전 음 저장

    for chord in chord_progression:
        scale = get_scale_for_chord(chord)  # ✅ 코드에 맞는 스케일 가져오기
        note_duration_options = [0.25, 0.5, 0.75]  # 🎵 랜덤한 리듬 패턴 (16분음표, 8분음표, 점음표)

        for _ in range(4):  # ✅ 코드당 4개의 멜로디 음표 생성
            note = random.choice(scale)  # 랜덤 음 선택

            # 🎯 이전 음과 연결성을 높이기 위해 음 차이를 1~3반음 내로 제한
            if previous_note:
                possible_notes = [n for n in scale if abs(n - previous_note) <= 3]
                if possible_notes:
                    note = random.choice(possible_notes)

            # 🎵 옥타브 변화 추가 (랜덤하게 한 옥타브 위/아래 음 포함)
            if random.random() > 0.7:  # 30% 확률로 한 옥타브 위/아래 추가
                note += random.choice([-12, 12])

            note_duration = random.choice(note_duration_options)  # 🎶 랜덤한 음 길이 선택
            melody.append((note, start_time, start_time + note_duration))

            start_time += note_duration  # 다음 음표 타이밍
            previous_note = note  # 현재 음을 이전 음으로 저장

    return melody

# 🎵 AI가 생성한 코드 진행
ai_generated_chords = ["C Major", "G Major", "F Major", "E7", "A7", "D7", "G7"]

# ✅ 멜로디 생성
melody_data = generate_melody_from_chords(ai_generated_chords)

# ✅ 콘솔 출력 (먼저 확인)
print("🎶 생성된 멜로디 패턴:")
for note, start, end in melody_data:
    print(f"음 {note} | 시작 {start:.2f}s | 끝 {end:.2f}s")