# install.packages("rpca")
install.packages("rpca")
library(rpca)

# Load your CSV file
# 'header = FALSE' if your CSV is just numbers. Change to TRUE if you have frame names.
# using as.matrix() is crucial because rpca requires a matrix, not a dataframe.
# Read the CSV with proper header handling
raw <- read.csv(
  "frames_pixels.csv",
  header = TRUE,  # Keep headers
  stringsAsFactors = FALSE
)

# Check the structure
print("Original data dimensions:")
print(dim(raw))
print("Column names:")
print(names(raw))

# Extract only the V columns (frame data) and skip the first row if needed
# The first column is pixel indices, so we skip it
frame_columns <- raw[, grep("^frame_", names(raw)), drop = FALSE]

# Remove the first row if it contains header artifacts
# (since your CSV has 14401 rows but should have 14400)
if (nrow(frame_columns) == 14401) {
  frame_columns <- frame_columns[2:nrow(frame_columns), , drop = FALSE]
}

print("Frame columns dimensions:")
print(dim(frame_columns))

# Convert to numeric matrix
video_matrix <- as.matrix(frame_columns)
video_matrix <- apply(video_matrix, 2, function(col) as.numeric(as.character(col)))

# Check for non-numeric values
print(paste("NA values:", sum(is.na(video_matrix))))
print(paste("Infinite values:", sum(is.infinite(video_matrix))))

# Remove columns with NAs if any
if (sum(is.na(video_matrix)) > 0) {
  video_matrix <- video_matrix[, colSums(is.na(video_matrix)) == 0]
}

# Final check
print("Final video_matrix dimensions:")
print(dim(video_matrix))
print(paste("Is null:", is.null(video_matrix)))
print(paste("Length:", length(video_matrix)))

# Normalize/standardize your video matrix
video_matrix_scaled <- scale(video_matrix)
# Run Robust PCA.
result <- rpca(video_matrix_scaled)
# Extract the Matrices
L <- result$L  # Background (Low-Rank)
S <- result$S  # Foreground / Human (Sparse)

# Save specific frames to check results
frame_10_human <- S[, 10]

# save L and S for visualization
write.csv(L, "background_output.csv")
write.csv(S, "foreground_output.csv")
