import os
import pandas as pd
import matplotlib.pyplot as plt

csv_path = r"C:/Users/mandu/Desktop/train9/results.csv"

if not os.path.exists(csv_path):
    print(f"파일을 찾을 수 없습니다: {csv_path}")
    exit()

df = pd.read_csv(csv_path)

precision_col = next((col for col in df.columns if "precision" in col.lower()), None)
recall_col = next((col for col in df.columns if "recall" in col.lower()), None)
map50_col = next((col for col in df.columns if "map50" in col.lower() and "-95" not in col.lower()), None)
map50_95_col = next((col for col in df.columns if "map50-95" in col.lower()), None)

def smooth_curve(data, weight=0.9):
    smoothed = []
    last = data[0]
    for point in data:
        smoothed_val = last * weight + (1 - weight) * point
        smoothed.append(smoothed_val)
        last = smoothed_val
    return smoothed

plt.style.use("ggplot")

plt.figure(figsize=(12, 7))

if precision_col:
    plt.plot(df['epoch'], smooth_curve(df[precision_col]), label='Precision', marker='o', linestyle='-', linewidth=2, alpha=0.8)
if recall_col:
    plt.plot(df['epoch'], smooth_curve(df[recall_col]), label='Recall', marker='s', linestyle='-', linewidth=2, alpha=0.8)
if map50_col:
    plt.plot(df['epoch'], smooth_curve(df[map50_col]), label='mAP@50', marker='^', linestyle='-', linewidth=2, alpha=0.8)
if map50_95_col:
    plt.plot(df['epoch'], smooth_curve(df[map50_95_col]), label='mAP@50-95', marker='*', linestyle='-', linewidth=2, alpha=0.8)

plt.title("YOLO Training Performance", fontsize=14, fontweight='bold')
plt.xlabel("Epoch", fontsize=12)
plt.ylabel("Score", fontsize=12)
plt.legend(fontsize=10, loc='lower right')
plt.grid(True, linestyle='--', alpha=0.7)

output_path = "fire_detect_train9.jpg"
plt.savefig(output_path, dpi=300)
print(f"저장 완료: {output_path}")

plt.show()
