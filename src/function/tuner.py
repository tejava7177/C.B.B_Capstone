import numpy as np
import pyaudio

# 주파수와 음계 매핑
NOTE_FREQUENCIES = {
    "E2": 86.13,
    "A2": 107.67,
    "D3": 150.73,
    "G3": 193.80,
    "B3": 215.10,
    "E4": 329.63,
}

FORMAT = pyaudio.paInt16
CHANNELS = 2  # 스테레오
RATE = 44100
CHUNK = 4096


def get_closest_note_and_status(frequency):
    """
    주어진 주파수에서 가장 가까운 음계와 상태를 계산
    """
    closest_note = None
    closest_freq = None
    min_difference = float('inf')

    for note, freq in NOTE_FREQUENCIES.items():
        difference = abs(frequency - freq)
        if difference < min_difference:
            closest_note = note
            closest_freq = freq
            min_difference = difference

    if closest_freq:
        if frequency < closest_freq - 2:
            status = "음이 낮습니다."
        elif frequency > closest_freq + 2:
            status = "음이 높습니다."
        else:
            status = "적절합니다."
    else:
        status = "알 수 없는 음입니다."

    return closest_note, status


def measure_background_noise(stream, duration=1):
    """
    배경 노이즈 수준을 측정
    """
    print("Measuring background noise...")
    total_amplitude = 0
    sample_count = int(RATE / CHUNK * duration)

    for _ in range(sample_count):
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        total_amplitude += np.max(np.abs(data))

    background_noise_level = total_amplitude / sample_count
    print(f"Background noise level: {background_noise_level:.2f}")
    return background_noise_level


def tuner():
    """기타 튜너 기능"""
    p = pyaudio.PyAudio()

    # 오디오 장치 나열
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print(f"Device ID {i}: {dev['name']}, Max Input Channels: {dev['maxInputChannels']}")

    # 사용자 입력으로 장치 선택
    device_id = int(input("Enter the device ID to use: "))

    # 스트림 열기
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_id,
                    frames_per_buffer=CHUNK)

    # 배경 노이즈 측정
    background_noise_level = measure_background_noise(stream)
    effective_threshold = background_noise_level * 2.0  # 민감도를 배경 노이즈의 2배로 설정

    print("Play a note on your guitar. Press Ctrl+C to stop.")

    previous_frequencies = []
    try:
        while True:
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)

            # 스테레오 데이터를 모노로 변환
            mono_data = np.mean(data.reshape(-1, 2), axis=1).astype(np.int16)

            # 신호 진폭 계산
            amplitude = np.max(np.abs(mono_data))
            if amplitude < effective_threshold:  # 노이즈 필터링
                #print("유효한 입력 신호가 없습니다.")
                previous_frequencies.clear()  # 이전 상태 초기화
                continue

            # FFT 수행
            fft = np.fft.fft(mono_data)
            freqs = np.fft.fftfreq(len(fft), 1 / RATE)
            magnitudes = np.abs(fft)

            # 주요 주파수 계산
            positive_freqs = freqs[:len(freqs)//2]
            positive_magnitudes = magnitudes[:len(magnitudes)//2]
            peak_freq = positive_freqs[np.argmax(positive_magnitudes)]

            if not (80 <= peak_freq <= 1000):  # 기타 주파수 범위만
                #print("유효한 신호가 없습니다.")
                previous_frequencies.clear()
                continue

            # 연속 주파수 감지
            previous_frequencies.append(peak_freq)
            if len(previous_frequencies) > 3:
                previous_frequencies.pop(0)

            if len(set(map(lambda x: round(x, 1), previous_frequencies))) == 1:  # 3번 연속 동일 주파수
                note, status = get_closest_note_and_status(peak_freq)
                print(f"Detected Frequency: {peak_freq:.2f} Hz, Closest Note: {note}, Status: {status}")
                previous_frequencies.clear()  # 상태 출력 후 초기화

    except KeyboardInterrupt:
        print("Stopped tuner.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    tuner()