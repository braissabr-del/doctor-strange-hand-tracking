import cv2

video = cv2.VideoCapture("dr_1.mp4")

for i in range(0, 100, 10):
    video.set(cv2.CAP_PROP_POS_FRAMES, i)
    success, frame = video.read()

    if success:
        print(f"Frame {i} - Brilho: {frame.mean():.2f}")

video.release()