import h5py
import numpy as np

# HDF5 파일 경로 (필요에 따라 수정)
file_path = '/Volumes/Extreme SSD/lmd_matched_h5/O/Q/W/TROQWIK128F9336B3E.h5'

with h5py.File(file_path, 'r') as f:
    # 아티스트 용어와 가중치 읽기
    artist_terms = f['metadata/artist_terms'][()]
    # 만약 문자열이 bytes 형식이면 디코딩
    artist_terms = [term.decode('utf-8') if isinstance(term, bytes) else term for term in artist_terms]

    artist_terms_weight = f['metadata/artist_terms_weight'][()]

# 결과 출력
print("Artist Terms:")
print(artist_terms)

print("\nArtist Terms Weights:")
print(artist_terms_weight)

# 대표 장르(가장 큰 가중치를 가진 용어) 결정
dominant_index = np.argmax(artist_terms_weight)
print("\nDominant Genre:", artist_terms[dominant_index])