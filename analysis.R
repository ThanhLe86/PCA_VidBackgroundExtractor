# install.packages("rpca")
library(rpca)

# Load your CSV file
# 'header = FALSE' if your CSV is just numbers. Change to TRUE if you have frame names.
# using as.matrix() is crucial because rpca requires a matrix, not a dataframe.
video_matrix <- as.matrix(read.csv("frames_pixels.csv", header = FALSE))

# Run Robust PCA.
result <- rpca(video_matrix)

# Extract the Matrices
L <- result$L  # Background (Low-Rank)
S <- result$S  # Foreground / Human (Sparse)

# Save specific frames to check results
frame_10_human <- S[, 10]

# save L and S for visualization
write.csv(L, "background_output.csv")
write.csv(S, "foreground_output.csv")