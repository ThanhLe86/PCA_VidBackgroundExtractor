import pandas as pd
import numpy as np
import cv2
import os
import tempfile
import shutil

def reconstruct_rgb_frames_efficient(csv_r, csv_g, csv_b, output_dir, width, height, chunk_size=50000):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"--- Processing to: {output_dir} ---")
    
    with open(csv_r, 'r') as f:
        header = f.readline().strip().split(',')
        num_frames = len(header) - 1
    
    print(f"Detected {num_frames} frames. Resolution: {width}x{height}")
    
    temp_dir = tempfile.mkdtemp()
    temp_filename = os.path.join(temp_dir, 'temp_video_volume.dat')
    
    video_volume = np.memmap(temp_filename, dtype='uint8', mode='w+', 
                             shape=(num_frames, height, width, 3))

    print(f"Created temporary volume at {temp_filename}. Starting chunked processing...")

    reader_r = pd.read_csv(csv_r, chunksize=chunk_size)
    reader_g = pd.read_csv(csv_g, chunksize=chunk_size)
    reader_b = pd.read_csv(csv_b, chunksize=chunk_size)

    total_pixels = width * height
    processed_pixels = 0

    try:
        for chunk_r, chunk_g, chunk_b in zip(reader_r, reader_g, reader_b):
            data_r = chunk_r.iloc[:, 1:].values.astype(np.uint8)
            data_g = chunk_g.iloc[:, 1:].values.astype(np.uint8)
            data_b = chunk_b.iloc[:, 1:].values.astype(np.uint8)

            batch_len = len(data_r)
            start_idx = processed_pixels
            end_idx = start_idx + batch_len
            
            data_r_t = data_r.T
            data_g_t = data_g.T
            data_b_t = data_b.T
            
            flat_view = video_volume.reshape(num_frames, total_pixels, 3)
            
            flat_view[:, start_idx:end_idx, 0] = data_b_t 
            flat_view[:, start_idx:end_idx, 1] = data_g_t 
            flat_view[:, start_idx:end_idx, 2] = data_r_t 
            
            processed_pixels += batch_len
            print(f"Processed pixels: {processed_pixels}/{total_pixels} ({(processed_pixels/total_pixels)*100:.1f}%)", end='\r')

        print("\nCSV processing complete. Saving images...")

        for i in range(num_frames):
            frame = video_volume[i] 
            
            output_path = os.path.join(output_dir, f"frame_{i:04d}.png")
            cv2.imwrite(output_path, frame)
            
            if i % 10 == 0:
                print(f"Saved frame {i}/{num_frames}", end='\r')
        
        print(f"\nSaved all frames to {output_dir}")

    finally:
        del video_volume 
        try:
            shutil.rmtree(temp_dir)
            print("Cleanup complete.")
        except Exception as e:
            print(f"Warning: Could not delete temp file: {e}")

if __name__ == "__main__":
    bg_r = "placeholder/background_output_r.csv"
    bg_g = "placeholder/background_output_g.csv"
    bg_b = "placeholder/background_output_b.csv"

    fg_r = "placeholder/foreground_output_r.csv"
    fg_g = "placeholder/foreground_output_g.csv"
    fg_b = "placeholder/foreground_output_b.csv"

    og_r = "placeholder/frames_R.csv"
    og_g = "placeholder/frames_G.csv"
    og_b = "placeholder/frames_B.csv"

    WIDTH = 1920  
    HEIGHT = 1080 

    if os.path.exists(bg_r):
        reconstruct_rgb_frames_efficient(bg_r, bg_g, bg_b, "res/output_frames/output_background", WIDTH, HEIGHT)
    else:
        print(f"Skipping Background: {bg_r} not found.")

    if os.path.exists(fg_r):
        reconstruct_rgb_frames_efficient(fg_r, fg_g, fg_b, "res/output_frames/output_foreground", WIDTH, HEIGHT)
    else:
        print(f"Skipping Foreground: {fg_r} not found.")

    if os.path.exists(og_r):
        reconstruct_rgb_frames_efficient(og_r, og_g, og_b, "res/output_frames/output_og_frames", WIDTH, HEIGHT)
    else:
        print(f"Skipping Original: {og_r} not found.")