import pandas as pd
import numpy as np
from PIL import Image
import os
import cv2


def reconstruct_frames_from_transposed_csv(csv_file, output_dir='frames',
                                           frame_numbers=None, header='frame_'):
    """
    Reconstruct grayscale frames from transposed CSV (Frame columns).
    """
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_file)

    frame_columns = [col for col in df.columns if col.startswith(header)]

    # Use all frames if not specified
    if frame_numbers is not None:
        if header == "V":
            target_frames = [f"V{i+1}" for i in frame_numbers if f"V{i+1}" in frame_columns]
        else:
            target_frames = [f"{header}{i}" for i in frame_numbers if f"{header}{i}" in frame_columns]
    else:
        target_frames = frame_columns

    width, height = 160, 90  # known dimensions

    for frame_col in target_frames:
        pixels = df[frame_col].values.astype(np.uint8)
        img = pixels.reshape((height, width))

        # Extract the frame number
        if header == "V":
            frame_number = int(frame_col[1:]) - 1
        else:
            frame_number = int(frame_col.split("_")[1])

        out_path = os.path.join(output_dir, f"frame_{frame_number:04d}.png")
        Image.fromarray(img, mode="L").save(out_path)

    print(f"Saved {len(target_frames)} frames to: {output_dir}")


def make_video_from_frames(frame_dir, output_video="output.mp4", fps=30):
    """
    Builds a video from a directory of numbered PNG frames.
    """
    frames = sorted([f for f in os.listdir(frame_dir) if f.endswith(".png")])
    if len(frames) == 0:
        raise ValueError("No frames found in directory: " + frame_dir)

    # Read first frame for size
    first_frame = cv2.imread(os.path.join(frame_dir, frames[0]), cv2.IMREAD_GRAYSCALE)
    height, width = first_frame.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height), isColor=False)

    for name in frames:
        img = cv2.imread(os.path.join(frame_dir, name), cv2.IMREAD_GRAYSCALE)
        video.write(img)

    video.release()
    print(f"Video saved: {output_video}")


if __name__ == "__main__":
    # -----------------------------
    # FOREGROUND
    # -----------------------------
    fg_csv = "foreground_output.csv"
    fg_frames_dir = "foreground_frames"
    reconstruct_frames_from_transposed_csv(fg_csv, fg_frames_dir, header="frame_")

    make_video_from_frames(
        frame_dir=fg_frames_dir,
        output_video="foreground_video.mp4",
        fps=30
    )

    # -----------------------------
    # BACKGROUND
    # -----------------------------
    bg_csv = "background_output.csv"
    bg_frames_dir = "background_frames"
    reconstruct_frames_from_transposed_csv(bg_csv, bg_frames_dir, header="V")

    make_video_from_frames(
        frame_dir=bg_frames_dir,
        output_video="background_video.mp4",
        fps=30
    )
