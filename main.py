from pyrogram import Client, filters
from pyrogram.types import Message
from pymediainfo import MediaInfo

API_ID = "10471716"
API_HASH = "f8a1b21a13af154596e2ff5bed164860"
BOT_TOKEN = "6365859811:AAF1Aj_VrbdxS9aPED2PqjwRaeEi4fcm_JE"


app = Client("media_info_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_command(client, message: Message):
    start_message = (
        "Hello! I am a Media Info Bot. Send me any video-based document or video file, "
        "and I will provide you with detailed information about it.\n\n"
        "Just upload a video or send a document, and I'll do the rest!"
    )
    client.send_message(chat_id=message.chat.id, text=start_message)

@app.on_message(filters.document | filters.video)
def get_media_info(client, message: Message):
    media_file = client.download_media(message)

    try:
        media_info = MediaInfo.parse(media_file)

        if media_info and media_info.tracks:
            info_text = ""
            
            for track in media_info.tracks:
                if track.track_type == "General":
                    info_text += f"**File Name:** {track.file_name}\n"
                    info_text += f"**File Size:** {track.other[0].file_size}\n"
                    info_text += f"**Duration:** {track.other[0].duration_string}\n\n"
    
                elif track.track_type == "Audio" or track.track_type == "Text":
                    info_text += f"**{track.track_type} Stream - {track.track_id}**\n"
                    info_text += f"**Codec:** {track.codec}\n"
                    info_text += f"**Language:** {track.language}\n"
                    info_text += f"**Bitrate:** {track.bit_rate}\n\n"
    
            client.send_message(
                chat_id=message.chat.id,
                text=f"Media Information:\n\n{info_text}",
                reply_to_message_id=message.id,
                parse_mode="markdown"
            )

        else:
            client.send_message(
                chat_id=message.chat.id,
                text="Unable to retrieve media information.",
                reply_to_message_id=message.id
            )

    except Exception as e:
        client.send_message(
            chat_id=message.chat.id,
            text=f"Error retrieving media information: {str(e)}",
            reply_to_message_id=message.id
        )

app.run()
