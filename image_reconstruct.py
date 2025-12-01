import pandas as pd
import numpy as np
from PIL import Image
import os

def reconstruct_frames_from_transposed_csv(csv_file, output_dir='reconstructed_frames', frame_numbers=None, header='frame_'):
    """
    Reconstruct frames from transposed CSV format
    
    Args:
        csv_file: Path to the CSV file
        output_dir: Directory to save reconstructed images
        frame_numbers: List of specific frame numbers to reconstruct (None = all frames)
        header: Prefix for frame columns ('frame_' for 'frame_0', 'V' for 'V1', etc.)
    """
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Get frame column names (excluding first column which is pixel index)
    frame_columns = [col for col in df.columns if col.startswith(header)]
    
    # Determine which frames to reconstruct
    if frame_numbers is not None:
        if header == 'V':
            # For V columns: V1, V2, V3... (frame 0, 1, 2...)
            target_frames = [f'V{i+1}' for i in frame_numbers if f'V{i+1}' in frame_columns]
        else:
            # For frame_ columns: frame_0, frame_1, frame_2...
            target_frames = [f'{header}{i}' for i in frame_numbers if f'{header}{i}' in frame_columns]
    else:
        target_frames = frame_columns
    
    print(f"Total frames available: {len(frame_columns)}")
    print(f"Reconstructing {len(target_frames)} frames")
    
    # Image dimensions (160x90 from your original video)
    width, height = 160, 90
    
    # Reconstruct each frame
    for frame_col in target_frames:
        # Extract pixel values for this frame
        pixels = df[frame_col].values.astype(np.uint8)
        
        # Reshape to image dimensions
        image_array = pixels.reshape((height, width))
        
        # Create and save the image
        image = Image.fromarray(image_array, mode='L')
        if header == 'V':
            # V1 corresponds to frame 0, V2 to frame 1, etc.
            frame_number = int(frame_col[1:]) - 1
        else:
            # frame_0, frame_1, etc.
            frame_number = int(frame_col.split('_')[1])
        output_filename = os.path.join(output_dir, f'frame_{frame_number:04d}.png')
        image.save(output_filename)
        print(f"Saved {output_filename}")
    
    print(f"Frames saved to directory: {output_dir}")

def reconstruct_single_frame(csv_file, frame_number, output_file=None, header='frame_'):
    """
    Reconstruct a single frame and return the image
    
    Args:
        csv_file: Path to the CSV file
        frame_number: Frame number to reconstruct
        output_file: Optional path to save the image
        header: Prefix for frame columns ('frame_' or 'V')
    
    Returns:
        PIL Image object
    """
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Image dimensions (160x90)
    width, height = 160, 90
    
    # Extract pixel values for the specified frame
    if header == 'V':
        # V1 corresponds to frame 0, V2 to frame 1, etc.
        frame_col = f'V{frame_number + 1}'
    else:
        # frame_0, frame_1, etc.
        frame_col = f'{header}{frame_number}'
    
    if frame_col not in df.columns:
        if header == 'V':
            available_frames = [int(col[1:]) - 1 for col in df.columns if col.startswith(header)]
        else:
            available_frames = [int(col.split('_')[1]) for col in df.columns if col.startswith(header)]
        min_frame = min(available_frames) if available_frames else 0
        max_frame = max(available_frames) if available_frames else 0
        raise ValueError(f"Frame {frame_number} not found. Available frames: {min_frame}-{max_frame}")
    
    pixels = df[frame_col].values.astype(np.uint8)
    
    # Reshape to image dimensions
    image_array = pixels.reshape((height, width))
    
    # Create the image
    image = Image.fromarray(image_array, mode='L')
    
    # Save if output file specified
    if output_file:
        image.save(output_file)
        print(f"Frame {frame_number} saved as {output_file}")
    
    return image

# Example usage:
if __name__ == "__main__":
    csv_file = "foreground_output.csv"  # Replace with your actual CSV filename
    
    # Reconstruct first few frames
    try:
        # Create output directory
        output_dir = "back_reconstructed_frames"
        os.makedirs(output_dir, exist_ok=True)
        
        # For V columns (V1, V2, V3...)
        reconstruct_frames_from_transposed_csv(csv_file, output_dir, frame_numbers=[0, 1, 2, 3, 4], header='frame_')
        
        # Or for frame_ columns (frame_0, frame_1, frame_2...)
        # reconstruct_frames_from_transposed_csv(csv_file, output_dir, frame_numbers=[0, 1, 2, 3, 4], header='frame_')
        
        # Or reconstruct a single frame
        # image = reconstruct_single_frame(csv_file, frame_number=0, output_file='frame_0.png', header='V')
        # print("Frame 0 reconstructed and saved as frame_0.png")
        
    except Exception as e:
        print(f"Error: {e}")
