import os

# 이미지와 라벨 파일 경로 설정
images_dir = "C:/Users/mandu/Desktop/coco_dataset_yolo/train/images/"
labels_txt_path = "C:/Users/mandu/Desktop/coco/train2017.txt"

# train2017.txt 파일에서 이미지 파일 경로 읽어오기
with open(labels_txt_path, "r") as f:
    listed_images = set(line.strip().replace('./images/train2017/', '') for line in f)

# 이미지 파일 목록 가져오기
image_files = set(os.listdir(images_dir))

# 삭제할 이미지 목록 구하기 (txt 파일에 없는 이미지들)
images_to_delete = image_files - listed_images

# 삭제
for image_name in images_to_delete:
    image_path = os.path.join(images_dir, image_name)
    if os.path.isfile(image_path):
        os.remove(image_path)
        print(f"이미지 삭제됨: {image_name}")

print("삭제 완료!")
