import os

# 라벨과 이미지 파일 경로 설정
labels_dir = "C:/Users/mandu/Desktop/coco_dataset_yolo/train/labels"
valid_classes = {0, 1, 2, 3, 5, 6, 7}  # 남길 클래스 번호

# 모든 .txt 라벨 파일 확인
for label_file in os.listdir(labels_dir):
    # .txt 파일만 처리
    if label_file.endswith(".txt"):
        label_path = os.path.join(labels_dir, label_file)
        
        # 라벨 파일 열기
        with open(label_path, "r") as f:
            lines = f.readlines()
        
        # 유효한 클래스만 필터링
        filtered_lines = [line for line in lines if int(line.split()[0]) in valid_classes]
        
        # 라벨 파일에 필터링된 라인 저장
        if filtered_lines:  # 필터링된 라인이 있다면 파일을 덮어쓴다.
            with open(label_path, "w") as f:
                f.writelines(filtered_lines)
        else:
            # 클래스가 모두 지워진 경우 파일을 삭제
            os.remove(label_path)
            print(f"라벨 파일 삭제됨: {label_file}")

print("라벨 필터링 완료!")
