import os
import time

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

CLIENT_SECRET_FILE = r"C:\youtube_automation\config\client_secret_157983371311-ocvfbmjr93ph62237ld8vrjjqp4ku3ke.apps.googleusercontent.com.json"

VIDEO_FOLDER = r"C:\youtube_automation\videos"

UPLOADED_FOLDER = r"C:\youtube_automation\uploaded"

# ---------------- VIRAL HASHTAGS ----------------
VIRAL_HASHTAGS = """
#shorts #viral #trending #youtubeshorts #ai #story #cartoon
#viralvideo #shortvideo #ytshorts #explore #fyp #reels #subscribe
"""

video_files = [
    f for f in os.listdir(VIDEO_FOLDER)
    if f.endswith(".mp4")
]

if not video_files:
    print("No videos found!")
    exit()

selected_video = video_files[0]
video_path = os.path.join(VIDEO_FOLDER, selected_video)

print("Uploading:", selected_video)

flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRET_FILE,
    SCOPES
)

credentials = flow.run_console()

youtube = build("youtube", "v3", credentials=credentials)

# ---------------- TITLE ----------------
title = selected_video.replace(".mp4", "").replace("_", " ").title() + " 🔥"

# ---------------- DESCRIPTION ----------------
description = f"""
{title}

Watch this amazing video! Subscribe for more daily content.

{VIRAL_HASHTAGS}
"""

request_body = {
    "snippet": {
        "title": title,
        "description": description,
        "tags": [
            "automation",
            "youtube",
            "viral",
            "shorts",
            "trending",
            "ai story"
        ],
        "categoryId": "22"
    },
    "status": {
        "privacyStatus": "public"
    }
}

media_file = MediaFileUpload(video_path)

request = youtube.videos().insert(
    part="snippet,status",
    body=request_body,
    media_body=media_file
)

response = request.execute()
media_file.stream().close()

print("UPLOAD SUCCESSFUL!")
print("Uploaded:", selected_video)
print("Video ID:", response["id"])

# ---------------- MOVE FILE AFTER UPLOAD ----------------
if not os.path.exists(UPLOADED_FOLDER):
    os.makedirs(UPLOADED_FOLDER)

time.sleep(5)

new_location = os.path.join(UPLOADED_FOLDER, selected_video)

os.rename(video_path, new_location)

print("Video moved to uploaded folder.")
