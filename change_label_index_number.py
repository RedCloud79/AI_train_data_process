import os
from pathlib import Path

# 원본 라벨 폴더 및 변환된 라벨 저장 폴더 경로
# label_folder = Path(r"C:/Users/mandu/Desktop/coco_dataset_yolo/test/labels")
# output_folder = Path(r"C:/Users/mandu/Desktop/coco_dataset_yolo/test/labels_trans")
label_folder = Path(r"C:/Users/mandu/Desktop/Baton2.0.v5i.yolov11/valid/labels")
output_folder = Path(r"C:/Users/mandu/Desktop/Baton2.0.v5i.yolov11/valid/labels_trans")
output_folder.mkdir(exist_ok=True)  # 저장 폴더 생성

# 클래스 매핑 (변환 규칙)
class_mapping = {
    0: 11,
}

def process_labels():
    label_paths = list(label_folder.glob("*.txt"))  # .txt 파일 리스트 가져오기
    
    for label_path in label_paths:
        output_path = output_folder / label_path.name  # 변환된 파일 저장 경로
        new_lines = []

        with open(label_path, "r") as f:
            lines = f.readlines()
        
        for line in lines:
            parts = line.strip().split()
            class_id = int(parts[0])

            if class_id in class_mapping:
                new_class_id = class_mapping[class_id]
                new_lines.append(f"{new_class_id} " + " ".join(parts[1:]))  # 변경된 클래스 적용

        # 변환된 데이터가 있는 경우만 저장
        if new_lines:
            with open(output_path, "w") as f:
                f.write("\n".join(new_lines) + "\n")
            print(f"Saved: {output_path}")
        else:
            print(f"Skipped empty file: {label_path}")

process_labels()
