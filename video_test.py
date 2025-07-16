import cv2
import torch
import subprocess
import numpy as np
import random
from pathlib import Path
from ultralytics import YOLO

# 모델 경로 설정
model_path = r"C:/Users/mandu/Desktop/train24/weights/best.pt"

# YOLO 모델 로드
model = YOLO(model_path)

# 클래스별 색상 지정
num_classes = len(model.names)
colors = {i: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(num_classes)}

def detect_objects(video_path, output_path):
    cap = cv2.VideoCapture(video_path)  # 비디오 파일 열기
    
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
        "-crf", "23",
        output_path
    ]
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)
    
    print("Processing...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("처리 완료.")
            break
        
        # 객체 감지 수행
        results = model(frame)
        
        # 결과를 프레임에 적용
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = f"{model.names[cls]} {conf * 100:.1f}%"
                # label = f"{model.names[cls]}"
                color = colors[cls]
                
                # 둥근 사각형 경계 상자 그리기
                thickness = 3
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness, cv2.LINE_AA)
                
                # 반투명 배경 추가
                overlay = frame.copy()
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                label_x2 = x1 + label_size[0] + 10
                label_y2 = y1 - label_size[1] - 10
                cv2.rectangle(overlay, (x1, y1 - 25), (label_x2, y1), color, -1)
                frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
                
                # 텍스트 추가 (굵고 선명하게)
                cv2.putText(frame, label, (x1 + 5, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        
        ffmpeg_process.stdin.write(frame.tobytes())
    
    ffmpeg_process.stdin.flush()
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()
    
    cap.release()
    print(f"저장 완료: {output_path}")

# 동영상 파일 감지 및 저장 실행
detect_objects(r"C:/Users/mandu/Desktop/safety_model/glainder_test_1.mp4", r"C:/Users/mandu/Desktop/safety_model/glainder_test_1_person_fire.mp4")
