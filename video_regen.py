import cv2
import os

def create_video_from_images(image_folder, output_video_file, fps=30):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    
    # Sort files by the numeric part of the filename (e.g., frame_0, frame_1)
    images.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    if not images:
        print(f"No images found in {image_folder}")
        return

    # Read the first image to determine width and height
    frame_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(frame_path)
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    # 'mp4v' is a general option for .mp4. If it fails, try 'avc1'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video_file, fourcc, fps, (width, height))

    print(f"Writing {len(images)} frames to {output_video_file}...")

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    print("Done.")

if __name__ == "__main__":
    # Example usage for the folders created in the previous step
    create_video_from_images("res/output_foreground", "foreground.mp4", fps=30)