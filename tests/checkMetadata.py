import h5py

# 분석할 HDF5 파일 경로 (필요에 따라 경로를 수정하세요)
file_path = '/Volumes/Extreme SSD/lmd_matched_h5/A/A/A/TRAAAGR128F425B14B.h5'


# 파일을 열어서 최상위 키들을 출력하고, 재귀적으로 구조를 출력하는 코드
def print_structure(name, obj):
    # 각 객체의 이름과 타입을 출력합니다.
    print(f"{name} ({type(obj)})")
    # 만약 데이터셋인 경우, shape 정보도 출력합니다.
    if isinstance(obj, h5py.Dataset):
        print(f"  - Shape: {obj.shape}")


with h5py.File(file_path, 'r') as f:
    print("HDF5 파일의 최상위 키:")
    for key in f.keys():
        print(f"  - {key}")

    print("\nHDF5 파일 전체 구조:")
    f.visititems(print_structure)