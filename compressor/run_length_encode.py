import numpy as np
import struct
import os

def compress(matrix, filename):
    cleaned = np.nan_to_num(matrix, nan=0)
    flat_data = cleaned.flatten().astype(np.float64)
    if len(flat_data) == 0: return
    values = []
    counts = []
    
    if len(flat_data) > 0:
        current_val = flat_data[0]
        current_count = 1
        
        for i in range(1, len(flat_data)):
            if flat_data[i] == current_val:
                current_count += 1
            else:
                values.append(current_val)
                counts.append(current_count)
                current_val = flat_data[i]
                current_count = 1
        values.append(current_val)
        counts.append(current_count)

    with open(filename, 'wb') as f:
        f.write(struct.pack('II', matrix.shape[0], matrix.shape[1]))
        

        for val, count in zip(values, counts):
            f.write(struct.pack('hi', val, count))
            
    print(f"Saved compressed file: {filename}")

# # --- Test it ---
# # 1. Create a dummy sparse matrix (mostly zeros)
# S_dummy = np.zeros((1000, 1000), dtype=np.int16) 
# S_dummy[50, 50] = 255 # One white pixel
# S_dummy[50, 51] = 255 # Two white pixels

# # 2. Save Uncompressed (Standard .npy file)
# np.save("uncompressed.npy", S_dummy)
# size_original = os.path.getsize("uncompressed.npy")

# # 3. Save Compressed (Our Custom RLE)
# compress(S_dummy, "compressed.bin")
# size_compressed = os.path.getsize("compressed.bin")

# print(f"Original Size: {size_original / 1024:.2f} KB")
# print(f"Compressed Size: {size_compressed / 1024:.2f} KB")
# print(f"Reduction: {100 - (size_compressed/size_original)*100:.1f}%")