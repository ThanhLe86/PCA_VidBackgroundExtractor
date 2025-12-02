install.packages("rpca")
install.packages("data.table") # specific for fast reading
library(rpca)
library(data.table)

# fread is roughly 10-50x faster than read.csv
raw <- fread("frames_pixels.csv", header = TRUE)

# Drop pixel_index (first col) and convert to matrix
video_matrix <- as.matrix(raw[, -1])

# Normalize to 0-1 range for better numerical stability
video_matrix <- video_matrix / 255

print("Running RPCA...")

# vital: center=FALSE, scale=FALSE ensures L and S remain in image intensity space
# term.delta: convergence tolerance. 1e-5 is precise enough; default is stricter.
result <- rpca(video_matrix, term.delta = 1e-5)

L <- result$L  # Background
S <- result$S  # Foreground

# S contains negative values (shadows/darkening). 
S_visual <- abs(S) 

# Clamp values to 0-1 just in case
L[L < 0] <- 0; L[L > 1] <- 1
S_visual[S_visual < 0] <- 0; S_visual[S_visual > 1] <- 1

# Scale back to 0-255 for export
write.csv(L * 255, "background_output.csv", row.names = FALSE)
write.csv(S_visual * 255, "foreground_output.csv", row.names = FALSE)

print("Done.")