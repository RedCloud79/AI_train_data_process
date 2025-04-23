import os

# 라벨 파일들이 있는 경로
labels_dir = "C:/Users/mandu/Desktop/market_hight_train_v14/test/labels"

# 제외할 클래스 인덱스
exclude_index = 4

def delete_labels_with_class_index(directory, class_index):
    deleted_count = 0
    for file_name in os.listdir(directory):
        if file_name.endswith(".txt"):
            file_path = os.path.join(directory, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # 클래스 인덱스가 포함되어 있는지 확인
            if any(line.strip().startswith(str(class_index)) for line in lines):
                os.remove(file_path)
                deleted_count += 1
                print(f"Deleted (contains class {class_index}): {file_path}")

    print(f"\n총 {deleted_count}개의 라벨 파일이 삭제되었습니다.")

# 실행
delete_labels_with_class_index(labels_dir, exclude_index)
