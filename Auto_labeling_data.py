import cv2
import os
from pathlib import Path
from ultralytics import YOLO

model_path = r"C:/Users/mandu/Desktop/ai_data_video/yolo11m.pt"
model = YOLO(model_path)

image_folder = r"C:/Users/mandu/Desktop/ai_data_video/labeling_image/change_test" 
output_folder = r"C:/Users/mandu/Desktop/ai_data_video/labeling_image/change_test_label"
os.makedirs(output_folder, exist_ok=True)

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
        with open(txt_filename, "w") as f:
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                class_id = int(box.cls[0].item())
                
                x_center = (x1 + x2) / 2 / w
                y_center = (y1 + y2) / 2 / h
                width = (x2 - x1) / w
                height = (y2 - y1) / h

                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        print(f"Saved: {txt_filename}")

process_images()
