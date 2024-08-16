import cv2
import os

# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

def get_video_info(segment_path):

    cap = cv2.VideoCapture(segment_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open segment {segment_path}")
        return
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / frame_rate if frame_rate > 0 else 0
    
    print(f"Video Info for {segment_path}:")
    print(f"  Width: {width}")
    print(f"  Height: {height}")
    print(f"  Frame Rate: {frame_rate} fps")
    print(f"  Number of Frames: {frame_count}")
    print(f"  Duration: {duration} seconds\n")

    cap.release()


if __name__ == "__main__":

    video_path = r'videos\segment_0.ts'
    # get_video_info(video_path)

    output_dir = 'frames'
    os.makedirs(output_dir, exist_ok=True)


    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        exit(1)

    frame_count = 0

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        frame_filename = os.path.join(output_dir, f'frame_{frame_count:04d}.png')
        
        cv2.imwrite(frame_filename, frame)
        
        # print(f"Saved {frame_filename}")
        
        frame_count += 1

    cap.release()

    print("Saved all frames.")
