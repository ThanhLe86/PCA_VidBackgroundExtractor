import cv2
import os
import numpy as np

def reconstruct_video(bg_folder, fg_folder, orig_folder, output_file, fps=30, threshold=15):
    # Load background reference (frame 0)
    bg_images = sorted([f for f in os.listdir(bg_folder) if f.endswith(".png")])
    bg_frame = cv2.imread(os.path.join(bg_folder, bg_images[0])).astype(np.uint8)

    height, width, _ = bg_frame.shape

    # Load sparse foreground masks
    fg_images = sorted(
        [f for f in os.listdir(fg_folder) if f.endswith(".png")],
        key=lambda x: int(x.split('_')[1].split('.')[0])
    )

    # Prepare video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for fg_name in fg_images:
        frame_id = int(fg_name.split('_')[1].split('.')[0])

        fg_path = os.path.join(fg_folder, fg_name)
        orig_path = os.path.join(orig_folder, f"frame_{frame_id:04d}.png")

        fg_mask = cv2.imread(fg_path, cv2.IMREAD_GRAYSCALE)
        orig_frame = cv2.imread(orig_path).astype(np.uint8)

        # Threshold mask (your sparse PNGs are grayscale intensities)
        mask = fg_mask > threshold

        # Start with background
        reconstructed = bg_frame.copy()

        # Restore original colors at foreground locations
        reconstructed[mask] = orig_frame[mask]

        video.write(reconstructed)

    video.release()
    print(f"Saved reconstructed video to {output_file}")
if __name__ == "__main__":
    bg_folder = "res/output_frames/output_background"
    fg_folder = "res/output_frames/output_foreground"
    orig_folder = "res/output_frames/output_og_frames"
    output_file = "res/reconstructed.mp4"

    reconstruct_video(bg_folder, fg_folder, orig_folder, output_file, fps=30, threshold=15)