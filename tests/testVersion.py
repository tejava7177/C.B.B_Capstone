import librosa
import soundfile as sf
import numpy as np
import scipy
from pydub import AudioSegment

# ✅ 패키지 버전 출력
print("📌 Installed Library Versions:")
print(f"🔹 librosa version: {librosa.__version__}")
print(f"🔹 soundfile version: {sf.__version__}")
print(f"🔹 numpy version: {np.__version__}")
print(f"🔹 scipy version: {scipy.__version__}")

# ✅ 간단한 기능 테스트
try:
    # 🎵 librosa 테스트 (무음 신호 생성)
    sr = 22050  # 샘플링 레이트
    test_audio = np.zeros(sr)  # 1초 무음 신호

    # ✅ librosa → soundfile 변경
    sf.write("test_librosa.wav", test_audio, sr)
    print("✅ librosa 테스트 통과!")

    # 🔊 soundfile 테스트 (파일 저장 & 로드)
    sf.write("test_soundfile.wav", test_audio, sr)
    _, samplerate = sf.read("test_soundfile.wav")
    print(f"✅ soundfile 테스트 통과! (샘플링 레이트: {samplerate})")

    # 📏 numpy 테스트 (행렬 연산)
    test_matrix = np.array([[1, 2], [3, 4]])
    test_matrix_transpose = np.transpose(test_matrix)
    print("✅ numpy 테스트 통과!", test_matrix_transpose)

    # 📈 scipy 테스트 (FFT 변환)
    test_fft = scipy.fft.fft(test_audio)
    print("✅ scipy 테스트 통과!")

    # 🎧 pydub 테스트 (오디오 변환)
    silence = AudioSegment.silent(duration=1000)  # 1초 무음 생성
    silence.export("test_pydub.wav", format="wav")
    print("✅ pydub 테스트 통과!")

except Exception as e:
    print("❌ 테스트 실패:", e)