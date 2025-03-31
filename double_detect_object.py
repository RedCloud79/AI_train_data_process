import cv2
import torch
from ultralytics import YOLO

# 모델 경로 설정
model_path_1 = "C:/Users/mandu/Desktop/train73/weights/best.pt"
model_path_2 = "yolov8n.pt"

# Check for CUDA device and set it
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

# YOLO 모델 초기화
model_1 = YOLO(model_path_1).to(device)
model_2 = YOLO(model_path_2).to(device)

# 비디오 캡처
cap = cv2.VideoCapture("C:/Users/mandu/Desktop/test_3.mp4")  # 비디오 화면 출력
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,768)

# 클래스들의 집합 설정
classes_of_interest_1 = {'Fire', 'Black smoke', 'White smoke', 'Gray smoke', 'Cloud', 'Fog', 'Light'
                         , 'Sunlight', 'ShakeA', 'ShakeB', 'None'}
classes_of_interest_2 = {'car', 'motorcycle', 'stove', 'electric bulb', 'Heating device', 'cigarette'}  # 예시 클래스

while True:
    ret, frame = cap.read()  # 프레임 읽기
    if not ret:
        break

    # YOLO로 객체 감지
    results_1 = model_1(frame)
    results_2 = model_2(frame)

    # 감지된 객체 박스 그리기
    if isinstance(results_1, list):  # 'Results' 객체가 리스트인지 확인
        for res in results_1:
            if 'boxes' in res._keys:  # 개별 'Results' 객체에서 'boxes' 속성 확인
                boxes = res.boxes.data  # boxes 정보 가져오기
                if len(boxes) > 0:
                    for box in boxes:
                        class_id = int(box[5])  # 객체의 클래스 ID
                        class_name = model_1.names[class_id]  # 객체의 클래스명

                        if class_name in classes_of_interest_1:
                            x1, y1, x2, y2 = map(int, box[:4])
                            conf = box[4]

                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(frame, f"{class_name}: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        if 'boxes' in results_1._keys:  # 'Results' 객체에서 'boxes' 속성 확인
            boxes = results_1.boxes.data  # boxes 정보 가져오기
            if len(boxes) > 0:
                for box in boxes:
                    class_id = int(box[5])  # 객체의 클래스 ID
                    class_name = model_1.names[class_id]  # 객체의 클래스명

                    if class_name in classes_of_interest_1:
                        x1, y1, x2, y2 = map(int, box[:4])
                        conf = box[4]

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f"{class_name}: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if isinstance(results_2, list):  # 'Results' 객체가 리스트인지 확인
        for res in results_2:
            if 'boxes' in res._keys:  # 개별 'Results' 객체에서 'boxes' 속성 확인
                boxes = res.boxes.data  # boxes 정보 가져오기
                if len(boxes) > 0:
                    for box in boxes:
                        class_id = int(box[5])  # 객체의 클래스 ID
                        class_name = model_2.names[class_id]  # 객체의 클래스명

                        if class_name in classes_of_interest_2:
                            x1, y1, x2, y2 = map(int, box[:4])
                            conf = box[4]

                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(frame, f"{class_name}: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        if 'boxes' in results_2._keys:  # 'Results' 객체에서 'boxes' 속성 확인
            boxes = results_2.boxes.data  # boxes 정보 가져오기
            if len(boxes) > 0:
                for box in boxes:
                    class_id = int(box[5])  # 객체의 클래스 ID
                    class_name = model_2.names[class_id]  # 객체의 클래스명

                    if class_name in classes_of_interest_2:
                        x1, y1, x2, y2 = map(int, box[:4])
                        conf = box[4]

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f"{class_name}: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 결과 출력
    cv2.imshow("YOLO Detection", frame)

    if cv2.waitKey(1) == ord('q'):
        break

# 작업 완료 후 해제
cap.release()
cv2.destroyAllWindows()
