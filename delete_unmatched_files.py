import os

images_dir = "C:/Users/mandu/Desktop/coco_dataset_yolo/val/images"
labels_dir = "C:/Users/mandu/Desktop/coco_dataset_yolo/val/labels"

def get_file_names(directory):
    return {os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))}

image_names = get_file_names(images_dir)
label_names = get_file_names(labels_dir)

images_to_delete = image_names - label_names
labels_to_delete = label_names - image_names

def delete_files(directory, file_names):
    for file_name in file_names:
        for ext in (".jpg", ".png", ".txt"):
            file_path = os.path.join(directory, file_name + ext)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

# 이미지와 라벨 삭제 실행
delete_files(images_dir, images_to_delete)
delete_files(labels_dir, labels_to_delete)

print("Cleanup completed.")