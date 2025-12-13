# AI code
# No external library dependencies for RPCA to ensure stability

# --- 1. Efficient RPCA Function ---
robust_pca_chunk <- function(M, max_iter=50) {
  M <- M / 255 
  lam <- 1 / sqrt(max(dim(M)))
  tol <- 1e-5 # Loose tolerance for speed
  
  Y <- M
  norm_two <- svd(Y, nu=0, nv=0)$d[1]
  norm_inf <- max(abs(Y)) / lam
  dual_norm <- max(norm_two, norm_inf)
  Y <- Y / dual_norm
  
  mu <- 1.25 / norm_two
  mu_bar <- mu * 1e7
  rho <- 1.5
  
  L <- M * 0
  S <- M * 0
  
  for (k in 1:max_iter) {
    # Update L
    temp_T <- M - S + (1/mu) * Y
    s_svd <- svd(temp_T)
    d_thresh <- pmax(s_svd$d - (1/mu), 0)
    L <- s_svd$u %*% (d_thresh * t(s_svd$v))
    
    # Update S
    temp_S <- M - L + (1/mu) * Y
    S <- sign(temp_S) * pmax(abs(temp_S) - (lam/mu), 0)
    
    # Update Y
    Z <- M - L - S
    Y <- Y + mu * Z
    mu <- min(mu * rho, mu_bar)
    
    if (max(abs(Z)) < tol) break
  }
  
  # Return denormalized results
  return(list(L = L * 255, S = abs(S) * 255))
}

# --- 2. Stream Processor ---
process__csv <- function(input_path, out_bg, out_fg, chunk_size=2000) {
  message(paste("Processing:", input_path))
  
  if (!file.exists(input_path)) {
    stop(paste("File not found:", input_path))
  }
  
  # Open Read Connection
  con_in <- file(input_path, "r")
  
  # Open Write Connections
  con_bg <- file(out_bg, "w")
  con_fg <- file(out_fg, "w")
  
  # 1. Handle Header
  header_line <- readLines(con_in, n=1)
  header_parts <- unlist(strsplit(header_line, ","))
  
  writeLines(header_line, con_bg)
  writeLines(header_line, con_fg)
  
  # Count frames (columns - 1 for index)
  n_cols <- length(header_parts)
  
  total_rows_processed <- 0
  
  repeat {
    chunk_df <- read.table(con_in, nrows=chunk_size, sep=",", header=FALSE, 
                           colClasses="numeric", fill=TRUE)
    
    if (nrow(chunk_df) == 0) break

    indices <- chunk_df[, 1]
    data_mat <- as.matrix(chunk_df[, -1])
    
    # Run RPCA on this horizontal strip
    res <- robust_pca_chunk(data_mat)
    
    # Clamp results to 0-255
    L_out <- pmin(pmax(res$L, 0), 255)
    S_out <- pmin(pmax(res$S, 0), 255)
    
    df_bg <- data.frame(pixel_index=indices, L_out)
    df_fg <- data.frame(pixel_index=indices, S_out)
    
    write.table(df_bg, con_bg, sep=",", row.names=FALSE, col.names=FALSE, quote=FALSE)
    write.table(df_fg, con_fg, sep=",", row.names=FALSE, col.names=FALSE, quote=FALSE)
    
    total_rows_processed <- total_rows_processed + nrow(chunk_df)
    cat(sprintf("\rProcessed %d rows...", total_rows_processed))
  }
  
  close(con_in)
  close(con_bg)
  close(con_fg)
  cat("\nFinished file.\n")
}

# --- 3. Execution ---
CHUNK_SIZE <- 5000 

start_time <- Sys.time()
# Red Channel
process__csv("frames_R.csv", 
                  "placeholder/background_output_r.csv", 
                  "placeholder/foreground_output_r.csv", 
                  chunk_size=CHUNK_SIZE)

# Green Channel
process__csv("frames_G.csv", 
                  "placeholder/background_output_g.csv", 
                  "placeholder/foreground_output_g.csv", 
                  chunk_size=CHUNK_SIZE)

# Blue Channel
process__csv("frames_B.csv", 
                  "placeholder/background_output_b.csv", 
                  "placeholder/foreground_output_b.csv", 
                  chunk_size=CHUNK_SIZE)

execution_time <- end_time - start_time
print(execution_time)

message("All channels processed.")
