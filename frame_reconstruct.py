import pandas as pd
import numpy as np
import cv2
import os

def csv_to_images(csv_file, output_folder, width=160, height=90):
    print(f"Reading {csv_file}...")
    df = pd.read_csv(csv_file)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over columns (frames)
    for i, col_name in enumerate(df.columns):
        # Extract column, reshape to original image dimensions (Height, Width)
        pixel_data = df[col_name].values
        image = pixel_data.reshape((height, width))
        
        # Convert to 8-bit unsigned integer (0-255) for image saving
        image = image.astype(np.uint8)
        
        filename = os.path.join(output_folder, f"frame_{i:04d}.png")
        cv2.imwrite(filename, image)

    print(f"Saved {len(df.columns)} images to {output_folder}")

if __name__ == "__main__":
    # Ensure dimensions match those inframe_extractor.py
    W, H = 160, 90

    csv_to_images("foreground_output.csv", "res/output_foreground", width=W, height=H)
    csv_to_images("background_output.csv", "res/output_background", width=W, height=H)