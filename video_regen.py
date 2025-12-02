import cv2
import os
import numpy as np

def reconstruct_video(bg_folder, fg_folder, output_file, fps=30):
    # 1. Load the single background reference (Frame 0)
    bg_images = sorted([f for f in os.listdir(bg_folder) if f.endswith(".png")])
    if not bg_images:
        print("No background images found.")
        return
    
    bg_path = os.path.join(bg_folder, bg_images[0])
    bg_frame = cv2.imread(bg_path).astype(np.float32) # Float for accurate math
    height, width, _ = bg_frame.shape

    # 2. Load all foregrounds
    fg_images = sorted([f for f in os.listdir(fg_folder) if f.endswith(".png")],
                       key=lambda x: int(x.split('_')[1].split('.')[0]))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    print(f"Reconstructing {len(fg_images)} frames using 1 background...")

    for fg_name in fg_images:
        fg_path = os.path.join(fg_folder, fg_name)
        fg_frame = cv2.imread(fg_path).astype(np.float32)

        # 3. The Math: Original = Background + Foreground
        # Note: Since we saved 'abs(S)', this is an approximation.
        reconstructed = bg_frame + fg_frame

        # Clip values to 0-255 to stay in valid image range
        reconstructed = np.clip(reconstructed, 0, 255).astype(np.uint8)

        video.write(reconstructed)

    cv2.destroyAllWindows()
    video.release()
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    reconstruct_video("res/output_background", "res/output_foreground", "res/reconstructed.mp4")