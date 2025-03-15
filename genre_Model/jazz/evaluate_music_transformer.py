import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# 📌 MusicTransformer 불러오기 (위치 확인 필요!)
from music_transformer_model import MusicTransformer

# ✅ 저장된 모델 경로
model_path = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/music_transformer_jazz.keras"

# ✅ 모델 로드 (custom_objects 포함)
try:
    model = tf.keras.models.load_model(model_path, custom_objects={"MusicTransformer": MusicTransformer})
    print("🎵 모델 로드 완료!")
except Exception as e:
    print(f"❌ 모델 로드 실패: {e}")
    exit()

# ✅ 데이터 불러오기
dataset_dir = "/Users/simjuheun/Desktop/개인프로젝트/C.B.B/genre_Model/jazz/"
X_path = dataset_dir + "X_filtered.npy"
Y_path = dataset_dir + "y_filtered.npy"  # 파일명 확인!

if os.path.exists(X_path) and os.path.exists(Y_path):
    X = np.load(X_path)
    y = np.load(Y_path)
    print(f"📂 데이터 로드 완료! X.shape = {X.shape}, y.shape = {y.shape}")
else:
    print("❌ 데이터 파일이 존재하지 않습니다. 경로를 확인하세요.")
    exit()

# ✅ 데이터 차원 확인 후 모델 평가
if X.shape[1:] == (10,) and y.shape[1:] == (10,):
    loss, acc = model.evaluate(X, y)
    print(f"✅ 평가 결과 - Loss: {loss:.4f}, Accuracy: {acc:.4f}")
else:
    print(f"❌ 입력 데이터 차원 불일치! 모델이 기대하는 입력과 다름: {X.shape}, {y.shape}")
    exit()

# ✅ 학습 로그 불러오기
history_path = dataset_dir + "history.npy"
if os.path.exists(history_path):
    try:
        history = np.load(history_path, allow_pickle=True).item()

        # ✅ Loss & Accuracy 시각화
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(history.get('loss', []), label='Train Loss')
        plt.plot(history.get('val_loss', []), label='Validation Loss')
        plt.legend()
        plt.title('Loss')

        plt.subplot(1, 2, 2)
        plt.plot(history.get('accuracy', []), label='Train Accuracy')
        plt.plot(history.get('val_accuracy', []), label='Validation Accuracy')
        plt.legend()
        plt.title('Accuracy')

        plt.show()
    except Exception as e:
        print(f"❌ 학습 로그를 불러오는 중 오류 발생: {e}")
else:
    print("🚨 학습 로그(history.npy)가 존재하지 않습니다.")