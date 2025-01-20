import numpy as np
import pyaudio

# 베이스 주파수와 음계 매핑
NOTE_FREQUENCIES = {
    "C": 129.20,
    "D": 150.73,
    "E": 86.13,
    "F": 86.13,
    "G": 96.90,
    "A": 107.67,
    "B": 118.43,
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


def list_audio_devices(p):
    """
    사용 가능한 오디오 입력 장치를 나열
    """
    print("사용 가능한 오디오 입력 장치:")
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev["maxInputChannels"] > 0:
            print(f"Device ID {i}: {dev['name']}, Max Input Channels: {dev['maxInputChannels']}")


def read_simple_chord():
    """
    간단한 코드 읽기 및 감지
    """
    p = pyaudio.PyAudio()

    # 오디오 장치 나열 및 선택
    list_audio_devices(p)
    while True:
        try:
            device_id = int(input("사용할 장치의 Device ID를 입력하세요: "))
            dev = p.get_device_info_by_index(device_id)
            if dev["maxInputChannels"] > 0:
                break
            else:
                print("유효하지 않은 장치입니다. 입력 채널이 있는 장치를 선택하세요.")
        except (ValueError, IOError):
            print("올바른 Device ID를 입력하세요.")

    # 스트림 열기
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_id,
                    frames_per_buffer=CHUNK)

    print("음을 연주하세요. (Ctrl+C로 종료)")

    previous_frequencies = []
    try:
        while True:
            # 오디오 데이터 읽기
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)

            # 스테레오 데이터를 모노로 변환
            mono_data = np.mean(data.reshape(-1, 2), axis=1).astype(np.int16)

            # FFT 수행
            fft = np.fft.fft(mono_data)
            freqs = np.fft.fftfreq(len(fft), 1 / RATE)
            magnitudes = np.abs(fft)

            # 양수 주파수만 사용
            positive_freqs = freqs[:len(freqs)//2]
            positive_magnitudes = magnitudes[:len(magnitudes)//2]

            # 주요 주파수 계산
            peak_freq = positive_freqs[np.argmax(positive_magnitudes)]

            if not (80 <= peak_freq <= 1000):  # 유효한 주파수 범위
                continue

            # 연속 주파수 감지
            previous_frequencies.append(peak_freq)
            if len(previous_frequencies) > 3:
                previous_frequencies.pop(0)

            if len(set(map(lambda x: round(x, 1), previous_frequencies))) == 1:  # 3번 연속 동일 주파수
                note, status = get_closest_note_and_status(peak_freq)
                print(f"Detected Frequency: {peak_freq:.2f} Hz, Closest Note: {note}입니다")
                previous_frequencies.clear()  # 상태 출력 후 초기화

    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    read_simple_chord()