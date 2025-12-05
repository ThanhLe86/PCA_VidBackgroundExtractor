# DevLog for analysis.R

## Packages and Dependencies
* **rpca**: Used for performing Robust Principal Component Analysis.
* **data.table**: Used specifically for the `fread()` function to rapidly load large CSV files, addressing the major performance bottleneck encountered with `read.csv()`.

## Data Handling and Preprocessing
1.  **Fast Loading**: The input file ("frames_pixels.csv") is loaded using `fread()` to efficiently handle the wide matrix structure (many columns/frames).
2.  **Matrix Conversion**: The first column ("pixel_index") is dropped, and the remaining data is converted to a numeric matrix (`video_matrix`) for RPCA.
3.  **Normalization**: The entire `video_matrix` is divided by 255. This step normalizes the raw pixel intensities (0-255) to the range [0, 1]. This scaling is performed externally to the `rpca` function call and improves the numerical stability of the RPCA algorithm.

## Robust PCA Execution
* **Function Call**: The RPCA is executed on the normalized `video_matrix`.
* **Parameter Optimization**: The function is called without the `center` or `scale` arguments, as the installed `rpca` package version did not recognize them. The data scaling was handled manually in the preprocessing step.
* **Convergence Speed**: The `term.delta` parameter is set to `1e-5` to slightly loosen the convergence tolerance compared to the default, resulting in significantly faster execution times.

## Post-Processing and Output
1.  **Matrix Extraction**: The Low-Rank matrix ($L$, representing the **Background**) and the Sparse matrix ($S$, representing the **Foreground/Movement**) are extracted from the RPCA result.
2.  **Foreground Visualization**: The absolute value of $S$ (`abs(S)`) is taken to create `S_visual`. This is necessary because $S$ contains signed values (negative for dark movements, positive for bright movements), and the absolute value ensures the magnitude of movement is captured for clear visualization.
3.  **Clamping**: Both $L$ and $S\_visual$ are clamped to the [0, 1] range to handle any minor numerical overshoots from the RPCA computation.
4.  **Final Export**: $L$ and $S\_visual$ are scaled back to the 0-255 range and saved as separate CSV files (`background_output.csv` and `foreground_output.csv`) without row names.

## How_to_run
### If you want the final product to be greyscaled
- Place the test video in the "assets" folder
- In the Greyscaled folder:
    - Run frame_extractor.py
    - Run analysis.R
    - Run frame_reconstruct.py, the reconstructed frames will be saved as .png images in the /res directory

### If you want the final product to be in full color
- Place the test video in the "assets" folder
- In the Full_Color folder:
    - Run RGB_extractor.py
    - Run rgb_analysis.R
    - Run RGB_frame_regen.py, the reconstructed frames will be saved as .png images in the /res directory

- If desired, run video_regen.py
