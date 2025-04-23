import os
from tqdm import tqdm

def check_label_consistency(label_dir):
    inconsistent_files = []

    label_files = [f for f in os.listdir(label_dir) if f.endswith(".txt")]

    for file_name in tqdm(label_files, desc="Checking labels"):
        file_path = os.path.join(label_dir, file_name)
        with open(file_path, 'r') as f:
            lines = f.readlines()

        num_boxes = 0
        num_segments = 0

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue  # 잘못된 라인 무시

            if len(parts) == 5:
                num_boxes += 1
            elif len(parts) >= 6 and len(parts) % 2 == 1:
                num_segments += 1

        if num_boxes > 0 and num_segments > 0:
            if num_boxes != num_segments:
                print(f"[WARNING] {file_name} ➜ boxes: {num_boxes}, segments: {num_segments}")
                inconsistent_files.append(file_name)

    print(f"\n총 불일치 파일 수: {len(inconsistent_files)}")
    return inconsistent_files

# 사용 예시
label_path = "C:/Users/mandu/Desktop/integration_model_v1/train/labels"
check_label_consistency(label_path)
