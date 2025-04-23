import cv2
import torch
import subprocess
import numpy as np
import random
from pathlib import Path
from ultralytics import YOLO

# 모델 경로 설정
model_path = r"C:/Users/mandu/Documents/GitHub/AI_train_data_process/fire_detect_model_v2/best.pt"

# YOLO 모델 로드
model = YOLO(model_path)

# 클래스별 색상 지정
num_classes = len(model.names)
colors = {i: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(num_classes)}

def detect_objects(video_path, output_path, target_classes=None):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-pix_fmt", "bgr24",
        "-s", f"{frame_width}x{frame_height}",
        "-r", str(fps),
        "-i", "-",
        "-an",
        "-vcodec", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "15",
        output_path
    ]
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

    print("Processing...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("처리 완료.")
            break

        results = model(frame)

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0].item())
                class_name = model.names[cls]

                # 🎯 선택된 클래스만 표시
                if target_classes and class_name not in target_classes:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                label = f"{class_name} {conf * 100:.1f}%"
                color = colors[cls]

                thickness = 3
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness, cv2.LINE_AA)

                overlay = frame.copy()
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                label_x2 = x1 + label_size[0] + 10
                label_y2 = y1 - label_size[1] - 10
                cv2.rectangle(overlay, (x1, y1 - 25), (label_x2, y1), color, -1)
                frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

                cv2.putText(frame, label, (x1 + 5, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        ffmpeg_process.stdin.write(frame.tobytes())

    ffmpeg_process.stdin.flush()
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()

    cap.release()
    print(f"저장 완료: {output_path}")

detect_objects(
    r"C:/Users/mandu/Documents/GitHub/AI_train_data_process/화재 진압 실험_250409_e1.mp4",
    r"C:/Users/mandu/Documents/GitHub/AI_train_data_process/화재 진압 실험_250409_e2.mp4",
    target_classes=["Fire"]
)

