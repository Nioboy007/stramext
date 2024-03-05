from pyrogram import Client, filters
import os
import subprocess

API_ID = 10471716
API_HASH = 'f8a1b21a13af154596e2ff5bed164860'
BOT_TOKEN = '6365859811:AAF1Aj_VrbdxS9aPED2PqjwRaeEi4fcm_JE'

app = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_message(client, message):
    message.reply_text("Welcome to the Video Bot! Send me any video file, and I'll extract audio and subtitle streams for you.")

@app.on_message(filters.video)
def process_video(client, message):
    video_path = message.video.file_id + ".mp4"
    audio_path = message.video.file_id + ".mp3"
    subtitle_path = message.video.file_id + ".srt"

    # Download the video
    video_file = client.download_media(message.video.file_id, file_name=video_path)

    # Extract audio using ffmpeg
    subprocess.run(["ffmpeg", "-i", video_file, "-vn", "-acodec", "libmp3lame", audio_path])

    # Extract subtitle using ffmpeg
    subprocess.run(["ffmpeg", "-i", video_file, subtitle_path])

    # Send extracted streams back to the user
    with open(audio_path, "rb") as audio_file:
        message.reply_audio(audio_file)

    with open(subtitle_path, "rb") as subtitle_file:
        message.reply_document(subtitle_file)

    # Clean up temporary files
    os.remove(video_file)
    os.remove(audio_path)
    os.remove(subtitle_path)

app.run()
