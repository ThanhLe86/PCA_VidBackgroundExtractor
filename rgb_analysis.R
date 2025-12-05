# install.packages("rpca")
# install.packages("data.table") # specific for fast reading
library(rpca)
library(data.table)

rawR <- fread("frames_R.csv", header = TRUE)
rawG <- fread("frames_G.csv", header = TRUE)
rawB <- fread("frames_B.csv", header = TRUE)

# Drop pixel_index 
matrix_R <- as.matrix(rawR[, -1])
matrix_G <- as.matrix(rawG[, -1])
matrix_B <- as.matrix(rawB[, -1])

# Normalize to 0-1 range
matrix_R <- matrix_R / 255
matrix_G <- matrix_G / 255
matrix_B <- matrix_B / 255

print("Running RPCA...")

start_time <- Sys.time()
resultR <- rpca(matrix_R, term.delta = 1e-5)
resultG <- rpca(matrix_G, term.delta = 1e-5)
resultB <- rpca(matrix_B, term.delta = 1e-5)
end_time <- Sys.time()
execution_time <- end_time - start_time
print(execution_time)

Lr <- resultR$L  # Background
Sr <- resultR$S  # Foreground

Lg <- resultG$L  # Background
Sg <- resultG$S  # Foreground

Lb <- resultB$L  # Background
Sb <- resultB$S  # Foreground

Sr_visual <- abs(Sr) 
Sg_visual <- abs(Sg) 
Sb_visual <- abs(Sb) 

Lr[Lr < 0] <- 0; Lr[Lr > 1] <- 1
Sr_visual[Sr_visual < 0] <- 0; Sr_visual[Sr_visual > 1] <- 1

Lg[Lg < 0] <- 0; Lg[Lg > 1] <- 1
Sg_visual[Sg_visual < 0] <- 0; Sg_visual[Sg_visual > 1] <- 1

Lb[Lb < 0] <- 0; Lb[Lb > 1] <- 1
Sb_visual[Sb_visual < 0] <- 0; Sb_visual[Sb_visual > 1] <- 1

write.csv(Lr * 255, "background_output_r.csv", row.names = FALSE)
write.csv(Sr_visual * 255, "foreground_output_r.csv", row.names = FALSE)

write.csv(Lg * 255, "background_output_g.csv", row.names = FALSE)
write.csv(Sg_visual * 255, "foreground_output_g.csv", row.names = FALSE)

write.csv(Lb * 255, "background_output_b.csv", row.names = FALSE)
write.csv(Sb_visual * 255, "foreground_output_b.csv", row.names = FALSE)

print("Done.")