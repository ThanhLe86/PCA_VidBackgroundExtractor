import cv2
import csv
import numpy as np

def save_csv(filename, data, total_frames):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        header = ["pixel_index"] + [f"frame_{i}" for i in range(total_frames)]
        writer.writerow(header)
        for i, row in enumerate(data):
            writer.writerow([i] + row.tolist())


def frame_extraction():
    video_path = "assets/Aura.mp4"

    csv_R = "frames_R.csv"
    csv_G = "frames_G.csv"
    csv_B = "frames_B.csv"

    w = 160
    h = 90

    R_frames = []
    G_frames = []
    B_frames = []

    total_frames = 0

    vid = cv2.VideoCapture(video_path)

    while True:
        ret, frame = vid.read()
        if not ret:
            break

        resized = cv2.resize(frame, (w, h))

        # cv2.split splits into B, G, R channels
        B, G, R = cv2.split(resized)

        R_frames.append(R.flatten())
        G_frames.append(G.flatten())
        B_frames.append(B.flatten())

        total_frames += 1

    vid.release()

    # pixel rows × frame columns
    R_data = np.array(R_frames).T
    G_data = np.array(G_frames).T
    B_data = np.array(B_frames).T
    save_csv(csv_R, R_data, total_frames)
    save_csv(csv_G, G_data, total_frames)
    save_csv(csv_B, B_data, total_frames)

    print("Saved:")
    print(f"- {csv_R}")
    print(f"- {csv_G}")
    print(f"- {csv_B}")


if __name__ == "__main__":
    frame_extraction()
