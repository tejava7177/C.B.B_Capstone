import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from music21 import chord


# 1. 오디오 파일 로드 및 시각화
def load_and_visualize_audio(file_path, div=None):
    """
    오디오 파일을 로드하고 스테레오 데이터의 일부를 시각화.

    Args:
        file_path (str): 분석할 오디오 파일 경로
        div (int): 샘플링 데이터의 길이 제한 (None일 경우 전체 데이터 사용)

    Returns:
        y (np.ndarray): 오디오 데이터 (스테레오 또는 모노)
        sr (int): 샘플링 레이트
    """
    # 오디오 파일 로드 (스테레오 모드로 로드)
    stereo, sr = librosa.load(file_path, sr=None, mono=False)  # mono=False: 스테레오 데이터 유지

    # div가 설정된 경우 데이터 제한
    if div is not None:
        stereo = stereo[:, :div]

    # 스테레오 데이터 시각화
    fig, axs = plt.subplots(2, 1, figsize=(14, 8))

    # 왼쪽 채널 (L)
    librosa.display.waveshow(stereo[0], sr=sr, ax=axs[0], color="blue")
    axs[0].set_title("Left Channel")

    # 오른쪽 채널 (R)
    librosa.display.waveshow(stereo[1], sr=sr, ax=axs[1], color="red")
    axs[1].set_title("Right Channel")

    plt.tight_layout()
    plt.show()

    return stereo, sr


# 2. 주파수 분석 (FFT) 및 시각화
def analyze_frequency(y, sr):
    # 입력 데이터가 스테레오인 경우 첫 번째 채널만 사용
    if y.ndim == 2:
        y = y[0]

    fft = np.fft.fft(y)
    frequencies = np.fft.fftfreq(len(fft), 1 / sr)
    magnitude = np.abs(fft)

    plt.figure(figsize=(14, 5))
    plt.plot(frequencies[:len(frequencies) // 2], magnitude[:len(magnitude) // 2])  # 양수 주파수만 표시
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.show()


# 3. 피치 추출 및 시각화
def extract_pitch(y, sr):
    # 입력 데이터가 스테레오인 경우 첫 번째 채널만 사용
    if y.ndim == 2:
        y = y[0]

    f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    times = librosa.times_like(f0, sr=sr)

    plt.figure(figsize=(14, 5))
    plt.plot(times, f0, label='F0', color='r')
    plt.title("Pitch Tracking")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.show()
    return f0, times


# 4. 코드 추출
def extract_chords(f0):
    def hz_to_note_name(frequency):
        """주파수를 노트 이름으로 변환"""
        return librosa.hz_to_note(frequency) if frequency else None

    # NaN 값을 제거
    cleaned_f0 = [freq for freq in f0 if not np.isnan(freq)]

    notes = [hz_to_note_name(freq) for freq in cleaned_f0]
    if len(notes) >= 3:
        detected_chord = chord.Chord(notes[:3])  # 첫 3개의 노트로 코드 감지
        print("Detected Chord:", detected_chord.commonName)
    else:
        print("Not enough notes to detect a chord.")
    return notes


# 5. 실행 함수
def main():
    file_path = 'testChord.wav'  # 분석할 오디오 파일 경로 입력
    div = 100000  # 분석할 샘플 길이 제한 (필요에 따라 설정)

    # 오디오 로드 및 시각화
    y, sr = load_and_visualize_audio(file_path, div)

    # 주파수 분석
    analyze_frequency(y, sr)

    # 피치 추출
    f0, times = extract_pitch(y, sr)

    # 코드 추출
    notes = extract_chords(f0)

    # 시간별 노트 출력
    print("\nDetected Notes:")
    for t, n in zip(times, notes):
        if n:
            print(f"Time: {t:.2f}s - Note: {n}")


# 메인 실행
if __name__ == "__main__":
    main()