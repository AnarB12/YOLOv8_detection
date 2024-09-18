import cv2
import time
import os
import logging
from datetime import datetime
from multiprocessing import Process

#************************************************************************************
def setup_logging():
    log_directory = './logs'
    os.makedirs(log_directory, exist_ok=True)
    log_filename = os.path.join(log_directory, f"{datetime.now().strftime('%Y-%m-%d')}.log")
    
    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging setup complete.")
    # print("Logging setup complete.")


def record_stream(url, output_file='output.avi', codec='XVID', fps=20.0, duration=60,
                  skip_frames=5, display=False):
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

    logging.info(f"Starting recording from {url}")
    print(f"Starting recording from {url}")

    vcap = cv2.VideoCapture(url)
    if not vcap.isOpened():
        logging.error("Error: Could not open video stream.")
        print("Error: Could not open video stream.")
        return

    frame_width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)

    logging.info(f"Video stream opened successfully. Resolution: {frame_width}x{frame_height}")
    print(f"Video stream opened successfully. Resolution: {frame_width}x{frame_height}")
    
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

    start_time = time.time()
    frame_count = 0

    while True:
        ret, frame = vcap.read()
        if not ret:
            logging.error("Failed to capture frame. Exiting.")
            # print("Failed to capture frame. Exiting.")
            break

        if frame_count % skip_frames == 0:
            out.write(frame)
            # logging.info(f"Frame {frame_count} recorded.")
            if display:
                cv2.imshow('Frame', frame)

        frame_count += 1
        elapsed_time = time.time() - start_time

        if elapsed_time >= duration:
            # logging.info("Recording duration reached. Stopping the recording.")
            # print("Recording duration reached. Stopping the recording.")
            break

        if display:
            if cv2.waitKey(22) & 0xFF == ord('q'):
                logging.info("Recording interrupted by user.")
                # print("Recording interrupted by user.")
                break

    vcap.release()
    out.release()

    if display:
        cv2.destroyAllWindows()

    logging.info(f"Recording completed. Elapsed time: {int(elapsed_time)} seconds")
    logging.info(f"Video saved to {output_file}")

    print(f"Recording completed. Elapsed time: {int(elapsed_time)} seconds")
    print(f"Video saved to {output_file}")

# Function to be run in each process
def record_camera(video_url, output_directory, codec, frames_per_second, record_duration, frame_skip, show_video):
    # Extract camera identifier from URL
    # For example, 'CAM72' from the URL
    camera_id = video_url.split('/')[-2]

    output_filename = f"recording_{camera_id}_{datetime.now().strftime('%Y%m%d_%H%M')}.avi"
    output_path = os.path.join(output_directory, output_filename)

    # Call the function with parameters from the User.
    record_stream(video_url, 
                  output_path, 
                  codec, 
                  frames_per_second, 
                  record_duration, 
                  frame_skip, 
                  show_video)

#********************************* Run the Main ***************************************

if __name__ == '__main__':
    setup_logging()
    
    video_urls = [
        'https://s2.ozarkstrafficoneview.com:443/rtplive/CAM72/playlist.m3u8',
        'https://sfs04-traveler.modot.mo.gov:443/rtplive/MODOT_CAM_309/playlist.m3u8',
        'https://s2.ozarkstrafficoneview.com:443/rtplive/CAM1017/playlist.m3u8',
        'https://s2.ozarkstrafficoneview.com:443/rtplive/CAM45/playlist.m3u8',
        # 'https://s2.ozarkstrafficoneview.com:443/rtplive/CAM64/playlist.m3u8',
        # 'https://s2.ozarkstrafficoneview.com:443/rtplive/CAM104/playlist.m3u8',
        # 'https://s2.ozarkstrafficoneview.com:443/rtplive/CAM128/playlist.m3u8',
        # 'https://s2.ozarkstrafficoneview.com:443/rtplive/CAM126/playlist.m3u8',
        # 'https://s2.ozarkstrafficoneview.com:443/rtplive/CAM52/playlist.m3u8'
    ]
    
    codec = 'XVID'
    frames_per_second = 20.0
    record_duration = 4000  # duration per camera in seconds
    frame_skip = 100
    show_video = False  # Set to False to avoid GUI-related issues
    
    now = datetime.now()
    date_folder = now.strftime('%Y-%m-%d')
    
    output_directory = os.path.join('./recordings', date_folder)
    os.makedirs(output_directory, exist_ok=True)
    
    logging.info(f"Created directory structure: {output_directory}")
    # print(f"Created directory structure: {output_directory}")
    
    logging.info(f"Recording video for the time segment: {now.strftime('%H%M')}")
    # print(f"Recording video for the time segment: {now.strftime('%H%M')}")
    
    processes = []
    for video_url in video_urls:
        p = Process(target=record_camera, args=(
            video_url, output_directory, codec, frames_per_second, record_duration, frame_skip, show_video))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
