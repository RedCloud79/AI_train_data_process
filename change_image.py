from pathlib import Path
from PIL import Image
src = Path(r"C:\Users\mandu\Desktop\parking\merge")
# src = Path(r"C:\Users\mandu\Desktop\Gaussian_data")
dst = src / "fixed"                                  # 변환 결과 폴더
dst.mkdir(exist_ok=True)

fail = 0
for p in sorted(src.glob("*.png")):  # 필요하면 "*.jpg" 등으로 바꿔도 됨
    try:
        img = Image.open(p)
        img.load()

        # 알파채널 있으면 유지, 없으면 RGB
        if img.mode in ("RGBA", "LA"):
            out = img.convert("RGBA")
        else:
            out = img.convert("RGB")

        out.save(dst / (p.stem + ".png"), "PNG", optimize=True)
    except Exception as e:
        print("FAIL:", p.name, e)
        fail += 1

print("done, failed =", fail)