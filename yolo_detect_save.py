import cv2
from ultralytics import YOLO
import subprocess
import numpy as np

model = YOLO("C:/Users/mandu/Desktop/ai_data_video/yolo11m.pt")

person_class = 0  # 사람 클래스 ID

def apply_mosaic(frame, bbox, mosaic_scale=0.05):
    h, w, _ = frame.shape
    x1, y1, x2, y2 = map(int, bbox)

    x1 = max(0, min(w, x1))
    y1 = max(0, min(h, y1))
    x2 = max(0, min(w, x2))
    y2 = max(0, min(h, y2))

    # 얼굴 영역이 너무 작으면 건너뜀
    if (y2 - y1) < 1 or (x2 - x1) < 1:
        return frame

    face = frame[y1:y2, x1:x2]
    
    # 얼굴이 비어있거나 너무 작은 영역이 오지 않도록 추가 검증
    if face.size == 0 or face.shape[0] < 2 or face.shape[1] < 2:
        return frame

    try:
        small = cv2.resize(face, None, fx=mosaic_scale, fy=mosaic_scale, interpolation=cv2.INTER_CUBIC)
        mosaic = cv2.resize(small, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
        frame[y1:y2, x1:x2] = mosaic
    except cv2.error as e:
        print(f"Resize error: {e}")
        return frame
    
    return frame

video_path = "C:/Users/mandu/Desktop/ai_data_video/kaachisan.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("비디오 파일을 열 수 없습니다.")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

output_path = "C:/Users/mandu/Desktop/ai_data_video/kaachisan_mosic.mp4"
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

    results = model(frame)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            cls = int(box.cls[0].cpu().numpy())
            if cls == person_class:
                # 얼굴 부분만 모자이크 적용 (상단 30%)
                face_y2 = y1 + (y2 - y1) * 0.3  # 상위 30%를 얼굴 영역으로 설정
                bbox = (x1, y1, x2, face_y2)
                
                # 모자이크 적용
                frame = apply_mosaic(frame, bbox, mosaic_scale=0.05)

    # 실시간으로 변환된 프레임 표시
    cv2.imshow('Processed Video', frame)

    # 'q' 키를 누르면 비디오 처리 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    ffmpeg_process.stdin.write(frame.tobytes())

ffmpeg_process.stdin.flush()
ffmpeg_process.stdin.close()
ffmpeg_process.wait()

cap.release()
cv2.destroyAllWindows()  # 모든 OpenCV 창 닫기
print(f"저장 완료: {output_path}")
