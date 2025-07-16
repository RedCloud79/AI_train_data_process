import os

# 확인할 라벨 폴더 경로
check_labels_dir = "C:/Users/mandu/Desktop/coco_data/train/check_labels"

# 라벨 파일 목록 가져오기
label_files = sorted(os.listdir(check_labels_dir))

# 잘못된 클래스 ID가 있는지 검사
unexpected_classes = set()
total_files = 0

for label_file in label_files:
    label_path = os.path.join(check_labels_dir, label_file)
    
    with open(label_path, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        class_id = int(line.split()[0])
        if class_id not in {0, 10}:
            unexpected_classes.add(class_id)
    
    total_files += 1

# 결과 출력
if unexpected_classes:
    print(f"⚠️ 예상치 못한 클래스 ID 발견: {unexpected_classes}")
else:
    print(f"✅ 모든 라벨 파일 확인 완료! 총 {total_files}개 파일이 모두 0 또는 10 클래스만 포함하고 있습니다.")
