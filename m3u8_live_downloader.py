"""
HTTP Live Streaming: https://datatracker.ietf.org/doc/html/rfc8216#autoid-56

Here are some of the concepts:

   - An M3U8 file is a playlist used in HTTP Live Streaming (HLS).
   - It contains references to video segments, which are small chunks 
     of the video (4-6 seconds in this playlist).
   - The M3U8 file can also point to different playlists (variant playlists) 
     that offer the same video at different quality levels.

   - The M3U8 file is updated regularly to include the latest segments as 
     the video is broadcasted.
   - The number of segments in the M3U8 file can change over time as new 
     segments are added and old ones are removed.
   - The script retrieves the latest segments and processes them.

   - The script downloads each segment from the live feed and saves them as 
     individual files.
   - It handles both direct segment URLs and variant playlists.

"""


import requests
import os
from urllib.parse import urljoin


# URL to the master playlist
m3u8_url = 'https://s2.ozarkstrafficoneview.com:443/rtplive/CAM72/playlist.m3u8'
response = requests.get(m3u8_url)
if response.status_code != 200:
    print(f"Download failed. Status code: {response.status_code}")
    exit(1)

# Parse the M3U8 content
m3u8_content = response.text
lines = m3u8_content.splitlines()

#*****************************************************************************
# Example Playlsit INFO:                                                     *
# EXTM3U                                                                     *
# EXT-X-VERSION:3                                                            *
# EXT-X-STREAM-INF:BANDWIDTH=246405,CODECS="avc1.42c00c",RESOLUTION=320x240  *
# chunklist_w1724579266.m3u8 (This will update)                              *
#                                                                            *
#*****************************************************************************


variant_url = None
for line in lines:
    if line.endswith('.m3u8') and not line.startswith('#'):
        variant_url = urljoin(m3u8_url, line)
        break

# If variant playlist found, load it
if variant_url:
    print(f"Variant playlist URL: {variant_url}")
    response = requests.get(variant_url)
    if response.status_code != 200:
        print(f"Failed to download variant M3U8 file. Status code: {response.status_code}")
        exit(1)
    m3u8_content = response.text
    lines = m3u8_content.splitlines()


# Variant Playlist URL: https://s2.ozarkstrafficoneview.com:443/rtplive/CAM72/chunklist_w1724579266.m3u8
# (It will update at each run and so will the segment URLs)

# Variant Playlist INFO:
# EXTM3U
# EXT-X-VERSION:3
# EXT-X-TARGETDURATION:12
# EXT-X-MEDIA-SEQUENCE:3140861
# EXT-X-DISCONTINUITY-SEQUENCE:47
# Example Segments:
# EXTINF:4.0,
# Segment URL: https://s2.ozarkstrafficoneview.com:443/rtplive/CAM72/media_w1724579266_3140861.ts
# EXTINF:6.0,
# Segment URL: https://s2.ozarkstrafficoneview.com:443/rtplive/CAM72/media_w1724579266_3140862.ts
# EXTINF:4.0,
# Segment URL: https://s2.ozarkstrafficoneview.com:443/rtplive/CAM72/media_w1724579266_3140863.ts


# Directory to write and save the segments
save_dir = 'videos'
os.makedirs(save_dir, exist_ok=True)


# Debugging - Print segment URIs
# print("Segment URIs:")
segments = []
for line in lines:
    if line.endswith('.ts') and not line.startswith('#'):
        segments.append(line)
        # print(f"Segment: {line}")


# Download each segment from the variant playlist
for i, segment in enumerate(segments):

    segment_url = urljoin(variant_url if variant_url else m3u8_url, 
                          segment)
    segment_name = os.path.join(save_dir, f'segment_{i}.ts')

    print(f"Downloading segment {i}: {segment_url}")

    response = requests.get(segment_url, stream=True)
    
    if response.status_code == 200:
        with open(segment_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        # print(f"Downloaded: {segment_name}")
    else:
        print(f"Failed to download segment {i}. Status code: {response.status_code}")

