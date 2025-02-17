import numpy as np
import json

# 저장된 numpy 파일 로드
chord_to_index = np.load("../chord_to_index.npy", allow_pickle=True).item()

# JSON 형식으로 보기 좋게 출력
print("🎼 코드 매핑 테이블:")
print(json.dumps(chord_to_index, indent=4, ensure_ascii=False))