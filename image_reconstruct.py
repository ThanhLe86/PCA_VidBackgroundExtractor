import pandas as pd
import numpy as np
from PIL import Image
import os

def reconstruct_single_frame(csv_file, frame_number, output_file=None):
    """
    Reconstruct a single frame and return the image
    
    Args:
        csv_file: Path to the CSV file
        frame_number: Frame number to reconstruct (0, 1, 2, ...)
        output_file: Optional path to save the image
    
    Returns:
        PIL Image object
    """
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Image dimensions (160x90 from your extraction script)
    width, height = 160, 90
    expected_pixels = width * height  # 14,400
    
    # Find the frame column - it should be V1, V2, V3, etc.
    # V1 corresponds to frame 0, V2 to frame 1, etc.
    frame_col = f'V{frame_number + 1}'  # V1 = frame 0, V2 = frame 1, etc.
    
    # Check if frame exists
    if frame_col not in df.columns:
        available_v_columns = [col for col in df.columns if col.startswith('V')]
        max_frame = len(available_v_columns) - 1 if available_v_columns else -1
        raise ValueError(f"Frame {frame_number} not found. Available frames: 0-{max_frame}")
    
    # Extract pixel values for the specified frame
    # Skip the first row if it contains header data that became a data row
    pixels = df[frame_col].values.astype(np.uint8)
    
    print(f"Raw pixel array shape: {pixels.shape}")
    
    # If we have 14401 pixels, the first one is likely extra - remove it
    if len(pixels) == 14401:
        pixels = pixels[1:]  # Remove first element
        print("Removed first element, now has 14400 pixels")
    elif len(pixels) != 14400:
        raise ValueError(f"Unexpected number of pixels: {len(pixels)}. Expected 14400.")
    
    # Reshape to image dimensions (90, 160)
    image_array = pixels.reshape((height, width))
    
    # Create the image
    image = Image.fromarray(image_array, mode='L')
    
    # Save if output file specified
    if output_file:
        image.save(output_file)
        print(f"Frame {frame_number} saved as {output_file}")
    
    return image

def reconstruct_multiple_frames(csv_file, frame_numbers, output_dir='reconstructed_frames'):
    """Reconstruct multiple frames"""
    os.makedirs(output_dir, exist_ok=True)
    
    for frame_num in frame_numbers:
        try:
            output_file = os.path.join(output_dir, f'frame_{frame_num:04d}.png')
            image = reconstruct_single_frame(csv_file, frame_num, output_file)
            print(f"Frame {frame_num} reconstructed successfully")
        except Exception as e:
            print(f"Error reconstructing frame {frame_num}: {e}")

# Example usage:
if __name__ == "__main__":
    csv_file = "foreground_output.csv"
    
    # Reconstruct first few frames
    try:
        # Reconstruct frame 0
        image = reconstruct_single_frame(csv_file, frame_number=0, output_file='frame_0.png')
        print("Frame 0 reconstructed and saved as frame_0.png")
        
        # Reconstruct frame 1
        image = reconstruct_single_frame(csv_file, frame_number=10, output_file='frame_1.png')
        print("Frame 1 reconstructed and saved as frame_1.png")
        
    except Exception as e:
        print(f"Error: {e}")
