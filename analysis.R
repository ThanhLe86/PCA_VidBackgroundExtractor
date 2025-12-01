# install.packages("rpca")
install.packages("rpca")
# Load the rpca library
library(rpca)

# Load your CSV file
# 'header = FALSE' if your CSV is just numbers. Change to TRUE if you have frame names.
# using as.matrix() is crucial because rpca requires a matrix, not a dataframe.
raw <- read.csv(
  "frames_pixels.csv",
  header = FALSE,
  stringsAsFactors = FALSE
)
video_matrix <- apply(raw, 2, function(col) as.numeric(col))


#check non numeric
sum(is.na(video_matrix))
sum(is.infinite(video_matrix))

#replace them with 0
video_matrix[is.na(video_matrix)] <- 0
video_matrix[is.infinite(video_matrix)] <- 0



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
