from pathlib import Path
from ultralytics.utils.downloads import download

# 직접 경로 지정
segments = True
dir = Path("C:/Users/mandu/Desktop")  # 원하는 경로로 바꿔도 됨

# 라벨 다운로드
base_url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/"
label_urls = [base_url + ("coco2017labels-segments.zip" if segments else "coco2017labels.zip")]
download(label_urls, dir=dir.parent)

# 이미지 다운로드 (필요할 경우)
# image_urls = [
#     "http://images.cocodataset.org/zips/train2017.zip",
#     "http://images.cocodataset.org/zips/val2017.zip",
#     "http://images.cocodataset.org/zips/test2017.zip",
# ]
# download(image_urls, dir=dir / "images", threads=3)
