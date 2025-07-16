import os
import shutil

# 원본 데이터 경로
images_dir = "C:/Users/mandu/Desktop/coco_data/valid/images"
labels_dir = "C:/Users/mandu/Desktop/coco_data/valid/labels"

# 저장할 폴더 경로
check_labels_dir = "C:/Users/mandu/Desktop/coco_data/valid/check_labels"
check_images_dir = "C:/Users/mandu/Desktop/coco_data/valid/check_images"

# 선택할 클래스 ID
selected_classes = {0, 10}

# 폴더 생성
os.makedirs(check_labels_dir, exist_ok=True)
os.makedirs(check_images_dir, exist_ok=True)

# 라벨 파일 목록 가져오기
label_files = sorted(os.listdir(labels_dir))

# 선택된 클래스가 포함된 라벨 및 이미지 복사
for label_file in label_files:
    label_path = os.path.join(labels_dir, label_file)
    image_path = os.path.join(images_dir, os.path.splitext(label_file)[0] + ".jpg")  # 이미지 확장자 확인 필요
    
    # 라벨 파일 읽기 및 필터링
    with open(label_path, "r") as f:
        lines = f.readlines()
    
    # 클래스 ID가 4 또는 5인 데이터만 추출
    filtered_lines = [line for line in lines if int(line.split()[0]) in selected_classes]
    
    # 필터링된 데이터가 있는 경우만 저장
    if filtered_lines:
        with open(os.path.join(check_labels_dir, label_file), "w") as f:
            f.writelines(filtered_lines)
        
        # 동일한 이름의 이미지 파일이 존재하면 복사
        if os.path.exists(image_path):
            shutil.copy(image_path, os.path.join(check_images_dir, os.path.basename(image_path)))

print("선택된 인덱스의 파일 복사가 완료되었습니다.")