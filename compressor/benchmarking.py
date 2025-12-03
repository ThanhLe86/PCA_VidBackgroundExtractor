import pandas as pd
import numpy as np
import scipy.sparse as sparse
import time
import os

def benchmark():
    input_csv = "frames_pixels.csv"
    bg_csv = "background_output.csv"
    fg_csv = "foreground_output.csv"
    
    if not os.path.exists(input_csv):
        return

    df = pd.read_csv(input_csv)
    data = df.iloc[:, 1:].values.astype(np.float64) / 255.0
    
    # 1. Original Compression
    t0 = time.time()
    np.savez_compressed("video_raw.npz", data=data)
    t_raw = time.time() - t0
    s_raw = os.path.getsize("video_raw.npz") / 1024

    # 2. RPCA Compression
    df_bg = pd.read_csv(bg_csv)
    df_fg = pd.read_csv(fg_csv)
    
    t0 = time.time()
    
    # Background: Use the first column/frame (Rank-1 assumption)
    bg_frame = df_bg.iloc[:, 0].values.astype(np.float64) / 255.0
    
    # Foreground: Use the full matrix and convert to sparse
    fg_matrix = df_fg.values.astype(np.float64) / 255.0
    
    fg_thresholded = np.where(np.abs(fg_matrix) < 0.05, 0, fg_matrix)
    
    fg_sparse = sparse.csc_matrix(fg_thresholded)
    
    with open("video_rpca.npz", 'wb') as f:
        np.savez_compressed(f, 
                            bg=bg_frame, 
                            fg_data=fg_sparse.data,
                            fg_indices=fg_sparse.indices,
                            fg_indptr=fg_sparse.indptr,
                            shape=fg_sparse.shape)
                            
    t_rpca = time.time() - t0
    s_rpca = os.path.getsize("video_rpca.npz") / 1024

    # 3. Results Output
    print(f"{'Method':<25}     | {'Time (s)':<10} | {'Size (KB)':<10}")
    print("-" * 50)
    print(f"{'Raw Data (Original)':<25}      | {t_raw:<10.4f} | {s_raw:<10.2f}")
    print(f"{'RPCA Output (1 BG + Sparse FG)':<25} | {t_rpca:<10.4f} | {s_rpca:<10.2f}")
    print("-" * 50)
    
    if s_rpca < s_raw:
        reduction = (1 - (s_rpca / s_raw)) * 100
        print(f"File Size Reduction: {reduction:.2f}%")

if __name__ == "__main__":
    benchmark()