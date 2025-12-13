import cv2
import pandas as pd
import numpy as np
import os

def extract_high_quality():
    video_path = "assets/video.mp4"
    
    # 1. Setup Video Capture
    cap = cv2.VideoCapture(video_path)
    
    # Get Original Dimensions (No Resizing!)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"Source Resolution: {width}x{height} at {fps} FPS")
    print("Warning: Processing at 100% scale will generate LARGE CSV files.")
    
    frames_r, frames_g, frames_b = [], [], []
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Split channels (OpenCV reads BGR)
        b, g, r = cv2.split(frame)
        
        # Flatten and append
        frames_r.append(r.flatten())
        frames_g.append(g.flatten())
        frames_b.append(b.flatten())
        
        frame_count += 1
        print(f"Extracted frame {frame_count}", end='\r')

    cap.release()
    print(f"\nExtraction complete. {frame_count} frames.")

    # 2. Helper to Save CSVs matching the R script's expected format
    def save_csv(data_list, channel):
        filename = f"frames_{channel}.csv"
        print(f"Formatting {channel.upper()} channel...")
        
        # Transpose: Rows = Pixels, Cols = Frames
        # using uint8 saves memory initially
        data = np.array(data_list, dtype=np.uint8).T
        
        df = pd.DataFrame(data)
        
        df.columns = [f"frame_{i}" for i in range(frame_count)]
        
        df.insert(0, "pixel_index", range(len(df)))
        
        print(f"Saving {filename} (this may take time)...")
        df.to_csv(filename, index=False)
        print(f"Saved {filename}")

    # 3. Write Files
    save_csv(frames_r, "R")
    save_csv(frames_g, "G")
    save_csv(frames_b, "B")

if __name__ == "__main__":
    extract_high_quality()