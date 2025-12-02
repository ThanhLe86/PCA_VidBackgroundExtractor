install.packages("rpca")
install.packages("data.table") # specific for fast reading
library(rpca)
library(data.table)

raw <- fread("frames_pixels.csv", header = TRUE)

# Drop pixel_index 
video_matrix <- as.matrix(raw[, -1])

# Normalize to 0-1 range
video_matrix <- video_matrix / 255

print("Running RPCA...")

result <- rpca(video_matrix, term.delta = 1e-5)

L <- result$L  # Background
S <- result$S  # Foreground

S_visual <- abs(S) 

L[L < 0] <- 0; L[L > 1] <- 1
S_visual[S_visual < 0] <- 0; S_visual[S_visual > 1] <- 1

write.csv(L * 255, "background_output.csv", row.names = FALSE)
write.csv(S_visual * 255, "foreground_output.csv", row.names = FALSE)

print("Done.")