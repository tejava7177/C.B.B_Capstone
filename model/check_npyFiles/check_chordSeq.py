import numpy as np

# 저장된 numpy 파일 로드
chord_sequences = np.load("../dataset/chord_sequences.npy")

# 첫 번째 10개의 코드 진행 출력
print("🎵 코드 진행 예시 (숫자 배열 형태):")
for seq in chord_sequences[:10]:
    print(seq)