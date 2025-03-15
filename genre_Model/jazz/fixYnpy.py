import numpy as np
import os

# ✅ 데이터 경로 설정
dataset_dir = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz"
files_to_fix = ["Y.npy", "y_filtered.npy"]

# ✅ 변환 함수 정의
def fix_npy(file_name):
    file_path = os.path.join(dataset_dir, file_name)

    if os.path.exists(file_path):
        # ✅ 파일 로드
        data = np.load(file_path)

        # ✅ 데이터 타입 확인
        print(f"📂 변환 전 {file_name} 타입: {data.dtype}, 샘플 데이터: {data[:5]}")

        # ✅ float(0~1) → int(0~127) 변환
        if data.dtype == np.float32 or data.dtype == np.float64:
            data = (data * 127).astype(np.int32)

            # ✅ 변환된 데이터 저장 (덮어쓰기)
            np.save(file_path, data)
            print(f"✅ 변환 완료: {file_name} (정수형 변환 완료!)")
        else:
            print(f"⚠️ 변환 불필요: {file_name} (이미 정수형)")

    else:
        print(f"🚨 파일 없음: {file_name}")

# ✅ 모든 파일 변환 실행
for file in files_to_fix:
    fix_npy(file)

print("🎵 모든 npy 파일 변환 완료!")