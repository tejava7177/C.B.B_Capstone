import tensorflow as tf
import numpy as np
import pretty_midi

# ✅ 악기별 모듈 가져오기
from inst.melody import generate_melody_and_rhythm
from inst.bass import generate_bassline
from inst.drums import generate_drum_pattern
from inst.comping import generate_chord_comping
from inst.brass import generate_brass_section
from inst.pad import generate_pad_sound

# ✅ 모델 로드
model_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/music_transformer_jazz.keras"
model = tf.keras.models.load_model(model_path, custom_objects={"MusicTransformer": MusicTransformer})
print("🎵 모델 로드 완료!")

# ✅ 코드 진행
chord_progression = np.array([
    [60, 64, 67],  # Cmaj7
    [67, 71, 74],  # Gmaj7
    [65, 68, 72],  # Fm
    [62, 65, 69],  # Dm
])

# ✅ 데이터 생성
generated_melody, generated_rhythm = generate_melody_and_rhythm(model, chord_progression)
generated_bassline, bass_rhythm = generate_bassline(chord_progression)
generated_drums, drum_rhythm = generate_drum_pattern(len(chord_progression))
generated_comping, comping_rhythm = generate_chord_comping(chord_progression)
generated_brass, brass_rhythm = generate_brass_section(chord_progression)
generated_pad, pad_rhythm = generate_pad_sound(chord_progression)

# ✅ MIDI 생성 및 저장
from midi_utils import create_midi  # 미디 생성 함수도 분리 가능
create_midi(generated_melody, generated_rhythm,
            generated_bassline, bass_rhythm,
            generated_drums, drum_rhythm,
            generated_comping, comping_rhythm,
            generated_brass, brass_rhythm,
            generated_pad, pad_rhythm,
            "generated_jazz.mid")