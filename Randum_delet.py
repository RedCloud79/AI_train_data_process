import os
import random

# 설정
folder_path = "C:/Users/mandu/Desktop/coco_data/train/check_images"  # 여기를 이미지 폴더 경로로 수정
keep_count = 32556  # 남길 이미지 개수
valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}  # 필요한 경우 추가 가능

# 파일 목록 가져오기
all_files = [f for f in os.listdir(folder_path)
             if os.path.splitext(f)[1].lower() in valid_extensions]

total_files = len(all_files)
print(f"총 이미지 수: {total_files}")

# 삭제할 수 없는 경우 처리
if total_files <= keep_count:
    print(f"이미지 수가 {keep_count}개 이하이므로 삭제하지 않습니다.")
else:
    # 무작위로 남길 파일 선택
    files_to_keep = set(random.sample(all_files, keep_count))
    
    # 삭제할 파일들
    files_to_delete = [f for f in all_files if f not in files_to_keep]

    for file_name in files_to_delete:
        file_path = os.path.join(folder_path, file_name)
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"{file_name} 삭제 실패: {e}")

    print(f"{len(files_to_delete)}개 이미지 삭제 완료. {keep_count}개 남김.")
