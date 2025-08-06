import cv2
import torch
from pathlib import Path
from ultralytics import YOLO

# 모델 경로 설정
model_path = r"C:/Users/mandu/Desktop/train24/weights/best.pt"

# YOLO 모델 로드
model = YOLO(model_path)

def detect_objects(video_path):
    cap = cv2.VideoCapture(video_path)  # 웹캠 또는 비디오 파일 열기
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 프레임 크기 조정
        frame = cv2.resize(frame, (1280, 960))
        
        # 객체 감지 수행
        results = model(frame)
        
        # 결과를 프레임에 적용
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = f"{model.names[cls]} {conf:.2f}"
                
                # 경계 상자 그리기
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow("YOLO Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# 동영상 파일 감지 실행
detect_objects(r"C:/Users/mandu/Desktop/safety_model/glainder_test_2.mp4")
# detect_objects(r"C:/Users/mandu/Desktop/화재 진압 실험_화재인식 모델/화재 진압 실험_250409_e1.mp4")
