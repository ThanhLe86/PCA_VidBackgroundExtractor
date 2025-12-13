import subprocess
import os
import sys

def run_step(command, step_name):
    print(f"\n[{step_name}] Starting...")
    try:
        subprocess.run(command, check=True)
        print(f"[{step_name}] Completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[{step_name}] Failed with error code {e.returncode}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[{step_name}] Failed: Executable not found. Check if Python/R is installed and in PATH.")
        sys.exit(1)

if __name__ == "__main__":
    if not os.path.exists("res/output_frames"):
        os.makedirs("res/output_frames")

    run_step([sys.executable, "Full_Color/RGB_extractor.py"], "1. Extraction")
    
    run_step(["Rscript", "Full_Color/rgb_analysis.R"], "2. RPCA Analysis")
    
    run_step([sys.executable, "Full_Color/RGB_frame_regen.py"], "3. Reconstruction")

    print("\nAll processing complete.")