import cv2
import os

def extract_frames(video_path, output_dir, frames_per_second):
    output_dir = output_dir.replace("\\", "/")
    os.makedirs(output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("None video")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("None fps")
        return
    
    frame_interval = int(fps / frames_per_second)
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            filename = os.path.join(output_dir, f"mapo_picture12_{saved_count:05d}.jpg").replace("\\", "/")
            if cv2.imwrite(filename, frame):
                saved_count += 1
        
        frame_count += 1
    
    cap.release()
    print(f"{saved_count}save the images.")

video_path = "C:/Users/mandu/Desktop/mapo_add_Light/irop-piro-fe01-c720_02i1y7.mp4"
# video_path = "C:/Users/mandu/Desktop/ai_data_video/longger_video/rgb_2024-01-26_03-08-54.mp4"
output_dir = "C:/Users/mandu/Desktop/mapo_add_Light/image_data/mapo_picture12/"
frames_per_second = 2

extract_frames(video_path, output_dir, frames_per_second)
