import cv2
import time
import os



def record_stream(url, output_file='output.avi', codec='XVID', fps=20.0, duration=60, 
                  skip_frames=5, display=True):
    
    """
    Records video from a stream and saves it to a file.
    
    Parameters:
        url (str): URL of the video stream (M3U8 playlist).
        output_file (str): Name of the output video file.
        codec (str): Codec used for saving the video.
        fps (float): Frames per second of the output video.
        duration (int): Duration of the recording in seconds.
        skip_frames (int): Number of frames to skip while recording.
        display (bool): Display the video frames during recording.
    """

    print(f"Starting recording from {url}")
    vcap = cv2.VideoCapture(url)
    if not vcap.isOpened():
        print("Error: Could not open video stream.")
        return

    frame_width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)

    print(f"Video stream opened successfully. Resolution: {frame_width}x{frame_height}")
    
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

    start_time = time.time()
    frame_count = 0

    while True:
        ret, frame = vcap.read()
        if not ret:
            print("Failed to capture frame. Exiting.")
            break

        if frame_count % skip_frames == 0:
            out.write(frame)
            # print(f"Frame {frame_count} recorded.")
            if display:
                cv2.imshow('Frame', frame)

        frame_count += 1
        elapsed_time = time.time() - start_time
        
        if elapsed_time >= duration:
            # print("Recording duration reached. Stopping the recording.")
            break

        if cv2.waitKey(22) & 0xFF == ord('q'):
            print("Recording interrupted by user.")
            break

    vcap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Recording completed. Elapsed time: {int(elapsed_time)} seconds")
    print(f"Video saved to {output_file}")



if __name__ == "__main__": 
    video_url = 'https://s2.ozarkstrafficoneview.com:443/rtplive/CAM72/playlist.m3u8'
    output_filename = 'recorded_video.avi'
    output_directory = './recordings'
    codec = 'XVID'  # Codec for encoding video
    frames_per_second = 20.0  # FPS for the output video
    record_duration = 60  # Duration to record in seconds
    frame_skip = 10  # Number of frames to skip during recording
    show_video = False  

    os.makedirs(output_directory, exist_ok=True)
    output_path = os.path.join(output_directory, output_filename)

    # Start recording
    record_stream(video_url, 
                  output_path, 
                  codec, 
                  frames_per_second, 
                  record_duration, 
                  frame_skip, 
                  show_video)
    

