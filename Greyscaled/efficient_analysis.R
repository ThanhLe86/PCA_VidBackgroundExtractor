robust_pca_chunk <- function(M, max_iter=50) {
  M <- M / 255 
  lam <- 1 / sqrt(max(dim(M)))
  tol <- 1e-5 
  
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
    temp_T <- M - S + (1/mu) * Y
    s_svd <- svd(temp_T)
    d_thresh <- pmax(s_svd$d - (1/mu), 0)
    L <- s_svd$u %*% (d_thresh * t(s_svd$v))
    
    temp_S <- M - L + (1/mu) * Y
    S <- sign(temp_S) * pmax(abs(temp_S) - (lam/mu), 0)
    
    Z <- M - L - S
    Y <- Y + mu * Z
    mu <- min(mu * rho, mu_bar)
    
    if (max(abs(Z)) < tol) break
  }
  
  return(list(L = L * 255, S = abs(S) * 255))
}

process_grayscale_csv <- function(input_path, out_bg, out_fg, chunk_size=2000) {
  message(paste("Processing:", input_path))
  
  if (!file.exists(input_path)) {
    stop(paste("File not found:", input_path))
  }
  
  con_in <- file(input_path, "r")
  con_bg <- file(out_bg, "w")
  con_fg <- file(out_fg, "w")
  
  header_line <- readLines(con_in, n=1)
  
  writeLines(header_line, con_bg)
  writeLines(header_line, con_fg)
  
  total_rows_processed <- 0
  
  repeat {
    chunk_df <- tryCatch({
      read.table(con_in, nrows=chunk_size, sep=",", header=FALSE, 
                 colClasses="numeric", fill=TRUE)
    }, error = function(e) {
      return(NULL)
    })
    
    if (is.null(chunk_df) || nrow(chunk_df) == 0) break

    indices <- chunk_df[, 1]
    data_mat <- as.matrix(chunk_df[, -1])
    
    res <- robust_pca_chunk(data_mat)
    
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

CHUNK_SIZE <- 5000 

start_time <- Sys.time()

process_grayscale_csv("placeholder/frames_pixels.csv", 
                      "placeholder/background_output.csv", 
                      "placeholder/foreground_output.csv", 
                      chunk_size=CHUNK_SIZE)

end_time <- Sys.time()
execution_time <- end_time - start_time
print(execution_time)

message("Grayscale processing complete.")