import cv2
import numpy as np
import pandas as pd
import os
from natsort import natsorted
from compressor import run_length_encode
# -------------------------------
# PARAMETERS
# -------------------------------
input_folder = "example 2/foreground_frames"  # folder containing RPCA sparse frames (grayscale)
output_folder = "postprocessed_frames"
os.makedirs(output_folder, exist_ok=True)

threshold_value = 30  # pixel intensity threshold for foreground
kernel_size = 3       # for morphological operations (3x3 kernel)
apply_smoothing = True
gaussian_ksize = 5    # size for Gaussian blur (must be odd)
temporal_smoothing = False
temporal_window = 3   # number of frames to average for temporal smoothing

# -------------------------------
# UTILITY FUNCTIONS
# -------------------------------

def load_frames(folder):
    files = natsorted([f for f in os.listdir(folder) if f.endswith(('.png', '.jpg'))])
    frames = [cv2.imread(os.path.join(folder, f), cv2.IMREAD_GRAYSCALE) for f in files]
    return frames, files

def save_frame(frame, filename):
    cv2.imwrite(filename, frame)

def postprocess_frame(frame, threshold=30, kernel_size=3, smooth=True, gauss_size=5):
    # Threshold to remove low-intensity noise
    _, fg_mask = cv2.threshold(frame, threshold, 255, cv2.THRESH_BINARY)

    # Morphological operations (closing to fill small holes and remove noise)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)  # optional

    # Gaussian smoothing
    if smooth:
        fg_mask = cv2.GaussianBlur(fg_mask, (gauss_size, gauss_size), 0)
        # Re-threshold after blur to keep binary mask
        _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)

    return fg_mask

# -------------------------------
# MAIN SCRIPT
# -------------------------------

frames, filenames = load_frames(input_folder)
processed_frames = []

for i, frame in enumerate(frames):
    processed = postprocess_frame(frame, threshold=threshold_value, 
                                  kernel_size=kernel_size, 
                                  smooth=apply_smoothing, 
                                  gauss_size=gaussian_ksize)
    processed_frames.append(processed)
    save_frame(processed, os.path.join(output_folder, filenames[i]))

# Optional temporal smoothing
if temporal_smoothing:
    temp_processed_frames = []
    half_window = temporal_window // 2
    for i in range(len(processed_frames)):
        start = max(0, i - half_window)
        end = min(len(processed_frames), i + half_window + 1)
        avg_frame = np.mean(processed_frames[start:end], axis=0).astype(np.uint8)
        _, avg_frame = cv2.threshold(avg_frame, 127, 255, cv2.THRESH_BINARY)
        temp_processed_frames.append(avg_frame)
        save_frame(avg_frame, os.path.join(output_folder, filenames[i]))
