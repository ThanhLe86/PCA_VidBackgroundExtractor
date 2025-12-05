import pandas as pd
import numpy as np
import cv2
import os

def reconstruct_rgb_frames(csv_r, csv_g, csv_b, output_dir, width=160, height=90):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Loading Red channel: {csv_r}...")
    df_r = pd.read_csv(csv_r)
    print(f"Loading Green channel: {csv_g}...")
    df_g = pd.read_csv(csv_g)
    print(f"Loading Blue channel: {csv_b}...")
    df_b = pd.read_csv(csv_b)

    # Ensure all channels have the same number of frames
    num_frames = min(len(df_r.columns), len(df_g.columns), len(df_b.columns))
    print(f"Reconstructing {num_frames} frames to {output_dir}...")

    for i in range(num_frames):
        # Extract the specific column (frame) for each channel
        col_r = df_r.iloc[:, i].values
        col_g = df_g.iloc[:, i].values
        col_b = df_b.iloc[:, i].values

        # Reshape flat arrays back to 2D image dimensions
        img_r = col_r.reshape((height, width))
        img_g = col_g.reshape((height, width))
        img_b = col_b.reshape((height, width))

        # Stack into a standard BGR image (OpenCV uses BGR, not RGB)
        img_bgr = np.dstack((img_b, img_g, img_r))

        # Ensure valid pixel range and type
        img_bgr = np.clip(img_bgr, 0, 255).astype(np.uint8)

        output_path = os.path.join(output_dir, f"frame_{i:04d}.png")
        cv2.imwrite(output_path, img_bgr)

    print("Done.")

if __name__ == "__main__":

    bg_r = "background_output_r.csv"
    bg_g = "background_output_g.csv"
    bg_b = "background_output_b.csv"

    fg_r = "foreground_output_r.csv"
    fg_g = "foreground_output_g.csv"
    fg_b = "foreground_output_b.csv"

    og_r = "frames_R.csv"
    og_g = "frames_G.csv"
    og_b = "frames_B.csv"

    # Reconstruct Background Frames
    print("--- Reconstructing Background ---")
    reconstruct_rgb_frames(bg_r, bg_g, bg_b, "res/output_background")

    # Reconstruct Foreground Frames
    print("\n--- Reconstructing Foreground ---")
    reconstruct_rgb_frames(fg_r, fg_g, fg_b, "res/output_foreground")

    print("\n--- Reconstructing Original Frames ---")
    reconstruct_rgb_frames(og_r, og_g, og_b, "res/output_og_frames")