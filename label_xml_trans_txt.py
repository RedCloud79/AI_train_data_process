import os
import xml.etree.ElementTree as ET

# 경로 설정
xml_dir = "C:/Users/mandu/Desktop/ai_data_video/mapo_fire_data/labels_xml"  # XML 파일이 있는 폴더
txt_dir = "C:/Users/mandu/Desktop/ai_data_video/mapo_fire_data/labels_yolo"  # YOLO txt 저장 폴더

# 클래스 매핑 (필요한 클래스 추가 가능)
class_mapping = {
    "Fire": 3,
    "None": 10,
    "White smoke": 2,
    "Light": 6
}

# YOLO 형식으로 변환하는 함수
def convert_to_yolo(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 이미지 크기 가져오기
    size = root.find("size")
    img_width = int(size.find("width").text)
    img_height = int(size.find("height").text)

    # 파일명 설정
    base_filename = os.path.splitext(os.path.basename(xml_file))[0]
    txt_path = os.path.join(txt_dir, base_filename + ".txt")

    with open(txt_path, "w") as txt_file:
        for obj in root.findall("object"):
            class_name = obj.find("name").text.strip()  # 클래스명 앞뒤 공백 제거

            # 클래스가 매핑 목록에 없으면 무시
            if class_name not in class_mapping:
                print(f"⚠️ 알 수 없는 클래스: {class_name} (무시됨) → {xml_file}")
                continue

            class_id = class_mapping[class_name]

            # 바운딩 박스 좌표 가져오기
            bndbox = obj.find("bndbox")
            xmin = int(bndbox.find("xmin").text)
            ymin = int(bndbox.find("ymin").text)
            xmax = int(bndbox.find("xmax").text)
            ymax = int(bndbox.find("ymax").text)

            # YOLO 형식 변환 (정규화)
            x_center = (xmin + xmax) / 2.0 / img_width
            y_center = (ymin + ymax) / 2.0 / img_height
            width = (xmax - xmin) / img_width
            height = (ymax - ymin) / img_height

            # YOLO 형식으로 저장
            txt_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

# 저장 폴더 생성
os.makedirs(txt_dir, exist_ok=True)

# XML 파일 변환 실행
for xml_file in os.listdir(xml_dir):
    if xml_file.endswith(".xml"):
        convert_to_yolo(os.path.join(xml_dir, xml_file))

print("✅ XML → YOLO 변환 완료!")
