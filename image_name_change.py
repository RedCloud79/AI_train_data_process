import os

def rename_images(folder_path):
    # 폴더 내 파일 목록 가져오기
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]
    
    # 정렬 (숫자가 포함된 경우를 대비하여 sorted 사용)
    files.sort()
    
    # 파일 이름 변경
    for idx, file in enumerate(files, start=1):
        old_path = os.path.join(folder_path, file)
        new_name = f"short_frame7_{idx}.jpg"
        new_path = os.path.join(folder_path, new_name)
        
        os.rename(old_path, new_path)
        print(f'Renamed: {old_path} -> {new_path}')

# 지정된 폴더 경로 사용
folder_path = "C:/Users/mandu/Desktop/ai_data_video/image_data/short_frame7/"
rename_images(folder_path)
