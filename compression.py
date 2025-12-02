from compressor import run_length_encode as rl_encoder
import pandas as pd
import numpy as np
import os

if __name__ == "__main__":
    df = pd.read_csv("res/example 2/foreground_output.csv", header=None, index_col=0)
    matrix = df.values
    matrix = matrix[1:, :]
    print(matrix)
    
    np.save("uncompressed.npy", df)
    size_original = os.path.getsize("uncompressed.npy")

    # 3. Save Compressed (Our Custom RLE)
    rl_encoder.compress(matrix, "compressed.bin")
    size_compressed = os.path.getsize("compressed.bin")

    print(f"Original Size: {size_original / 1024:.2f} KB")
    print(f"Compressed Size: {size_compressed / 1024:.2f} KB")
    print(f"Reduction: {100 - (size_compressed/size_original)*100:.1f}%")