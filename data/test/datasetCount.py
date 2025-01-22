import os

# 데이터셋 디렉토리 경로
dataset_path = "/Volumes/Extreme SSD/lmd_aligned"

# A~Z 디렉토리 탐색
for folder in sorted(os.listdir(dataset_path)):
    folder_path = os.path.join(dataset_path, folder)
    if os.path.isdir(folder_path):
        print(f"Folder: {folder}, File count: {len(os.listdir(folder_path))}")