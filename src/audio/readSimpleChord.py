import librosa
import numpy as np
import matplotlib.pyplot as plt


# 1. 오디오 파일 로드
def load_audio(file_path):
    """
    오디오 파일을 로드하여 샘플 데이터와 샘플링 레이트를 반환.

    Args:
        file_path (str): 분석할 오디오 파일 경로

    Returns:
        y (np.ndarray): 오디오 신호 데이터
        sr (int): 샘플링 레이트
    """
    y, sr = librosa.load(file_path, sr=None)
    return y, sr


# 2. 피치 추출
def extract_pitch(y, sr):
    """
    오디오 데이터에서 피치를 추출.

    Args:
        y (np.ndarray): 오디오 신호 데이터
        sr (int): 샘플링 레이트

    Returns:
        f0 (np.ndarray): 기본 주파수 배열 (Hz)
    """
    f0, _, _ = librosa.pyin(
        y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7')
    )
    return f0


# 3. 주파수를 노트로 변환
def frequency_to_notes(f0):
    """
    주파수를 음악 노트로 변환.

    Args:
        f0 (np.ndarray): 기본 주파수 배열 (Hz)

    Returns:
        notes (list): 감지된 노트의 리스트
    """

    def hz_to_note_name(freq):
        return librosa.hz_to_note(freq) if freq and not np.isnan(freq) else None

    notes = [hz_to_note_name(freq) for freq in f0 if freq and not np.isnan(freq)]
    return notes


# 4. 메인 실행
def main():
    file_path = 'e.wav'  # 분석할 WAV 파일 경로
    print(f"Analyzing audio file: {file_path}")

    # 1. 오디오 파일 로드
    y, sr = load_audio(file_path)

    # 2. 피치 추출
    f0 = extract_pitch(y, sr)

    # 3. 노트 변환
    notes = frequency_to_notes(f0)

    # 결과 출력
    print("\nDetected Notes:")
    for idx, note in enumerate(notes):
        print(f"{idx + 1}. {note}")

    # 사용자 입력 방식 (확장 가능)
    # print("\n사용자 입력 테스트:")
    # user_notes = []
    # for i in range(3):  # 최대 3개의 노트를 입력받음
    #     user_note = input(f"{i + 1}번째 노트를 입력해주세요: ")
    #     user_notes.append(user_note)
    #
    # print("\n사용자 입력 노트:", user_notes)


if __name__ == "__main__":
    main()