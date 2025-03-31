import cv2
import os
from pathlib import Path
from ultralytics import YOLO

model_path = r"C:/Users/mandu/Desktop/ai_data_video/yolo11m.pt"
model = YOLO(model_path)

image_folder = r"C:/Users/mandu/Desktop/coco_dataset_yolo/test/images" 
output_folder = r"C:/Users/mandu/Desktop/coco_dataset_yolo/test/labels"
os.makedirs(output_folder, exist_ok=True)

# 유효한 클래스 번호 설정 (0: person, 2: car, 3: motorcycle, 5: bus, 7: truck)
valid_classes = {0, 2, 3, 5, 7}

def process_images():
    image_paths = list(Path(image_folder).glob("*.jpg"))  # JPG 이미지 파일만 처리
    
    for image_path in image_paths:
        img = cv2.imread(str(image_path))
        h, w, _ = img.shape
        results = model(img)
        
        if len(results[0].boxes) == 0:  # 감지된 객체가 없을 경우
            os.remove(image_path)  # 이미지 삭제
            print(f"Deleted: {image_path}")
            continue  # 다음 이미지로 넘어감

        txt_filename = os.path.join(output_folder, image_path.stem + ".txt")
        valid_lines = []  # 유효한 라벨만 담을 리스트
        
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            class_id = int(box.cls[0].item())
            
            # 유효한 클래스만 처리
            if class_id in valid_classes:
                x_center = (x1 + x2) / 2 / w
                y_center = (y1 + y2) / 2 / h
                width = (x2 - x1) / w
                height = (y2 - y1) / h

                valid_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        # 유효한 라벨이 하나라도 있으면 .txt 파일에 저장
        if valid_lines:
            with open(txt_filename, "w") as f:
                f.writelines(valid_lines)
            print(f"Saved: {txt_filename}")
        else:
            # 유효한 클래스가 없다면 .txt 파일 삭제
            if os.path.exists(txt_filename):
                os.remove(txt_filename)
                print(f"Deleted empty label file: {txt_filename}")

process_images()
