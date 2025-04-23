import os

def check_label_consistency(label_dir):
    inconsistent_files = []

    for file_name in os.listdir(label_dir):
        if not file_name.endswith(".txt"):
            continue

        file_path = os.path.join(label_dir, file_name)
        with open(file_path, 'r') as f:
            lines = f.readlines()

        num_boxes = 0
        num_segments = 0

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue  # 잘못된 형식 무시
            num_boxes += 1
            if len(parts) > 5:
                num_segments += 1

        if num_boxes != num_segments and num_segments != 0:
            print(f"[WARNING] {file_name} ➜ boxes: {num_boxes}, segments: {num_segments}")
            inconsistent_files.append(file_name)

    print(f"\n총 불일치 파일 수: {len(inconsistent_files)}")
    return inconsistent_files

# 사용 예시
label_path = "C:/Users/mandu/Desktop/integration_model_v1/train/labels"
check_label_consistency(label_path)
