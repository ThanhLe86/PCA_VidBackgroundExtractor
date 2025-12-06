# !curl -L "https://github.com/JayLohokare/smart-traffic-signals/raw/refs/heads/master/video1.mp4" -o video.mp4

import cv2
import csv
import numpy as np

def frame_extraction():
    video_path = "assets/cctv.mp4"
    output_csv = "placeholder/frames_pixels.csv"
    output_video = "processed_video.mp4"

    # resize for less pixel variables
    new_width = 160
    new_height = 90

    cap = cv2.VideoCapture(video_path)

    # Get video properties for output video
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # Initialize video writer
    out = cv2.VideoWriter(output_video, fourcc, fps, (new_width, new_height), False)

    frames = []
    total_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        resized = cv2.resize(frame, (new_width, new_height))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        # Write processed frame to output video
        out.write(gray)

        flat_pixels = gray.flatten()

        frames.append(flat_pixels)
        total_frames += 1

    cap.release()
    out.release()  # Release the video writer

    data = np.array(frames)
    data_T = data.T

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)

        header = ["pixel_index"] + [f"frame_{i}" for i in range(total_frames)]
        writer.writerow(header)

        for i, row in enumerate(data_T):
            writer.writerow([i] + row.tolist())

    print(f"Saved CSV to: {output_csv}")
    print(f"Saved processed video to: {output_video}")

if __name__ == "__main__":
    frame_extraction()
