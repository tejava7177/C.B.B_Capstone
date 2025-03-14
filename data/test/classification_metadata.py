import os
import glob
import shutil
import h5py

# HDF5 파일 루트 디렉토리 (메타데이터)
h5_root = "/Volumes/Extreme SSD/lmd_matched_h5"
# 실제 MIDI 파일들이 있는 루트 디렉토리
midi_root = "/Volumes/Extreme SSD/lmd_matched"
# 분류된 결과를 저장할 출력 루트 디렉토리
output_root = "/Volumes/Extreme SSD/lmd_classified"

# 원하는 장르 카테고리 (모두 소문자로)
target_genres = ["jazz", "blues", "rock", "punk", "r&b"]

# 출력 디렉토리 생성 (각 장르별)
for genre in target_genres:
    genre_dir = os.path.join(output_root, genre)
    os.makedirs(genre_dir, exist_ok=True)

# HDF5 파일들을 재귀적으로 찾습니다.
h5_files = glob.glob(os.path.join(h5_root, "**", "*.h5"), recursive=True)
print(f"총 {len(h5_files)}개의 HDF5 파일을 찾았습니다.")

for h5_file in h5_files:
    # 트랙 ID: 파일명에서 확장자 제거 (예: TRAAAGR128F425B14B)
    track_id = os.path.splitext(os.path.basename(h5_file))[0]

    try:
        with h5py.File(h5_file, 'r') as f:
            if "metadata/artist_terms" in f:
                terms = f["metadata/artist_terms"][()]
                # bytes 형식이면 디코딩 후 소문자 변환
                terms = [term.decode('utf-8').lower() if isinstance(term, bytes) else term.lower() for term in terms]
            else:
                print(f"{track_id}: 'metadata/artist_terms'가 없습니다.")
                continue
    except Exception as e:
        print(f"{track_id} 파일을 여는 중 오류 발생: {e}")
        continue

    # target_genres 중 어느 것과 매칭되는지 확인합니다.
    matched_genres = []
    for genre in target_genres:
        # 만약 artist_terms 중 하나라도 genre 문자열이 포함되면 매칭
        if any(genre in term for term in terms):
            matched_genres.append(genre)

    if not matched_genres:
        # 원하는 장르와 매칭되지 않으면 건너뜁니다.
        continue

    # 해당 트랙의 MIDI 파일들이 저장된 디렉토리를 찾습니다.
    # HDF5 파일의 상대경로와 동일한 구조에서 track_id 폴더가 존재할 것으로 가정합니다.
    # 예를 들어, /Volumes/Extreme SSD/lmd_matched_h5/A/A/A/TRAAAGR128F425B14B.h5 에 대응하는
    # MIDI 디렉토리는 /Volumes/Extreme SSD/lmd_matched/A/A/A/TRAAAGR128F425B14B 입니다.
    # 먼저, h5 파일의 상대 경로(예: A/A/A/TRAAAGR128F425B14B.h5)를 구합니다.
    rel_path = os.path.relpath(h5_file, h5_root)
    # 상대 경로에서 파일명을 제외한 경로
    rel_dir = os.path.dirname(rel_path)
    # MIDI 디렉토리 경로 (track_id 폴더)
    midi_dir = os.path.join(midi_root, rel_dir, track_id)
    if not os.path.isdir(midi_dir):
        print(f"{track_id}: 해당 MIDI 디렉토리({midi_dir})를 찾을 수 없습니다.")
        continue

    # MIDI 디렉토리 내의 모든 .mid 파일을 찾습니다.
    midi_files = glob.glob(os.path.join(midi_dir, "*.mid"))
    if not midi_files:
        print(f"{track_id}: MIDI 파일이 없습니다.")
        continue

    # 매칭된 각 장르별로 MIDI 파일을 복사합니다.
    for genre in matched_genres:
        dest_dir = os.path.join(output_root, genre)
        for midi_file in midi_files:
            dest_file = os.path.join(dest_dir, os.path.basename(midi_file))
            try:
                shutil.copy(midi_file, dest_file)
                print(f"{track_id}: {os.path.basename(midi_file)} 복사됨 -> {genre}")
            except Exception as e:
                print(f"{track_id}: {os.path.basename(midi_file)}를 {genre} 폴더로 복사하는 중 오류: {e}")