import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment

# 1. 사인파 생성 함수
def generate_sine_wave(frequency, duration, sr=44100):
    """
    주어진 주파수로 사인파 생성
    :param frequency: 주파수 (Hz)
    :param duration: 길이 (초)
    :param sr: 샘플링 레이트
    :return: 사인파 numpy 배열
    """
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)  # 시간축
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # 진폭 0.5로 설정
    return sine_wave

# 2. 기본 설정
frequency = 440  # A4 음 (440Hz)
duration = 5  # 5초 길이
sampling_rate = 44100  # 샘플링 레이트

# 3. 사인파 생성
sine_wave = generate_sine_wave(frequency, duration, sr=sampling_rate)

# 4. WAV 파일 저장
wav_file = "output.wav"
sf.write(wav_file, sine_wave, sampling_rate)
print(f"WAV 파일 생성 완료: {wav_file}")

# 5. WAV -> MP3 변환
mp3_file = "output.mp3"
audio = AudioSegment.from_wav(wav_file)
audio.export(mp3_file, format="mp3")
print(f"MP3 파일 생성 완료: {mp3_file}")