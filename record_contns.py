import cv2
import time
import os
import logging
from datetime import datetime
from threading import Timer


def setup_logging():
    log_directory = './logs'
    os.makedirs(log_directory, exist_ok=True)
    log_filename = os.path.join(log_directory, f"{datetime.now().strftime('%Y-%m-%d')}.log")
    
    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging setup complete.")


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

    logging.info(f"Starting recording from {url}")
    vcap = cv2.VideoCapture(url)
    if not vcap.isOpened():
        logging.error("Error: Could not open video stream.")
        return

    frame_width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)

    logging.info(f"Video stream opened successfully. Resolution: {frame_width}x{frame_height}")
    
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

    start_time = time.time()
    frame_count = 0

    while True:
        ret, frame = vcap.read()
        if not ret:
            logging.error("Failed to capture frame. Exiting.")
            break

        if frame_count % skip_frames == 0:
            out.write(frame)
            if display:
                cv2.imshow('Frame', frame)

        frame_count += 1
        elapsed_time = time.time() - start_time

        if elapsed_time >= duration:
            logging.info("Recording duration reached. Stopping the recording.")
            break

        if cv2.waitKey(22) & 0xFF == ord('q'):
            logging.info("Recording interrupted by user.")
            break

    vcap.release()
    out.release()
    cv2.destroyAllWindows()

    logging.info(f"Recording completed. Elapsed time: {int(elapsed_time)} seconds")
    logging.info(f"Video saved to {output_file}")


def schedule_recordings(url, time_segments, codec='XVID', fps=20.0, duration=600, skip_frames=10, display=False):
    today_date = datetime.now().date()
    
    for start_time, end_time in time_segments:
        now = datetime.now()
        start = datetime.combine(today_date, datetime.strptime(start_time, "%H:%M").time())
        end = datetime.combine(today_date, datetime.strptime(end_time, "%H:%M").time())

        if start <= now <= end:
            segment_time = now.strftime('%H%M')
            date_folder = now.strftime('%Y-%m-%d')
            segment_folder = f"{date_folder}/{segment_time}"
            output_directory = os.path.join('./recordings', segment_folder)
            os.makedirs(output_directory, exist_ok=True)

            output_filename = f"recording_{now.strftime('%Y%m%d_%H%M')}.avi"
            output_path = os.path.join(output_directory, output_filename)

            logging.info(f"Scheduled recording for {start_time} to {end_time} in {output_path}")
            
            record_stream(url, output_path, codec, fps, duration, skip_frames, display)

    if datetime.now().date() == today_date:
        # Schedule the function to run again after 1 minute to keep checking the time
        Timer(60, schedule_recordings, [url, time_segments, codec, fps, duration, skip_frames, display]).start()
    else:
        logging.info("Stopping the script after completing today's schedule.")


if __name__ == "__main__":
    setup_logging()

    video_url = 'https://s2.ozarkstrafficoneview.com:443/rtplive/CAM72/playlist.m3u8'
    codec = 'XVID'  # Codec for encoding video
    frames_per_second = 20.0  # FPS for the output video
    record_duration = 600  # Duration to record in seconds (10 minutes)
    frame_skip = 10  # Number of frames to skip during recording
    show_video = False  # Set to True to display video during recording

    # Define the time segments as a list of tuples
    time_segments = [
        ("07:00", "09:00"),
        ("12:00", "13:00"),
        ("16:00", "17:00"),
        ("21:00", "22:00")
    ]

    # Pass the time segments to the scheduling function
    schedule_recordings(video_url, time_segments, codec, frames_per_second, record_duration, frame_skip, show_video)
