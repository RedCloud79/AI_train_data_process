import os
import shutil
import random

image_dir = "C:/Users/mandu/Desktop/ai_data_video/mapo_fire_data/images"
label_dir = "C:/Users/mandu/Desktop/ai_data_video/mapo_fire_data/labels"
output_dir = "C:/Users/mandu/Desktop/ai_data_video/mapo_fire_data/mapo_fire_dataset"

# 데이터 분할 비율
train_ratio = 0.7
valid_ratio = 0.2
test_ratio = 0.1

image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
random.shuffle(image_files)  # 랜덤 섞기

total_images = len(image_files)
train_count = int(total_images * train_ratio)
valid_count = int(total_images * valid_ratio)

train_files = image_files[:train_count]
valid_files = image_files[train_count:train_count + valid_count]
test_files = image_files[train_count + valid_count:]

def make_dirs(base_dir, categories):
    for category in categories:
        os.makedirs(os.path.join(base_dir, category, "images"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, category, "labels"), exist_ok=True)

make_dirs(output_dir, ["train", "valid", "test"])

def copy_files(file_list, src_img_dir, src_lbl_dir, dest_dir):
    for file in file_list:
        img_src = os.path.join(src_img_dir, file)
        lbl_src = os.path.join(src_lbl_dir, os.path.splitext(file)[0] + ".txt")  # 확장자 변환 개선

        img_dest = os.path.join(dest_dir, "images", file)
        lbl_dest = os.path.join(dest_dir, "labels", os.path.splitext(file)[0] + ".txt")

        shutil.copy(img_src, img_dest)
        
        if os.path.exists(lbl_src):
            shutil.copy(lbl_src, lbl_dest)
        else:
            print(f"라벨 파일 없음: {lbl_src}")  # 디버깅용 출력

copy_files(train_files, image_dir, label_dir, os.path.join(output_dir, "train"))
copy_files(valid_files, image_dir, label_dir, os.path.join(output_dir, "valid"))
copy_files(test_files, image_dir, label_dir, os.path.join(output_dir, "test"))

print("데이터 분할 완료!")
