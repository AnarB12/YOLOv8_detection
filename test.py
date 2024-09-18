import cv2 
import random

video_path = r'recordings\2024-08-29\1200\recording_20240829_1200.avi'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
random_frame_number = random.randint(0, total_frames - 1)

cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_number)
ret, frame = cap.read()

if ret:
    output_path = 'random_frame.jpg'  
    cv2.imwrite(output_path, frame)
    print('Random frame saved.')
else:
    print("Failed to save the frame")

cap.release()

# cap = cv2.VideoCapture(video_path)

# if not cap.isOpened():
#     print("Error: Could not open video.")
#     exit()

# # Frame
# frame_number = 0

# out_folder = 'Frames'
# os.makedirs(out_folder, exist_ok=True)

# while True:
#     ret, frame = cap.read()

#     if not ret:
#         break

#     frame_filename = f'{out_folder}/frame_{frame_number:04d}.jpg'
#     cv2.imwrite(frame_filename, frame)

#     # print(f'Saved {frame_filename}')

#     frame_number += 1

# print('Saved all frames.')
# cap.release()
# # cv2.destroyAllWindows()
