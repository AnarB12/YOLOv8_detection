@echo off
REM Activate the Anaconda environment
call "C:\Users\banar\anaconda3\Scripts\activate.bat" Deep_Learning

REM Navigate to the script's directory
cd "C:\Users\banar\OneDrive\Desktop\YOLO_Annotation"

REM Run the Python script
python record_video.py

REM Deactivate the Anaconda environment
call conda deactivate