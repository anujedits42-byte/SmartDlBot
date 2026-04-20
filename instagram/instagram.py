import os
import logging
import time
import asyncio
from pathlib import Path

import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Config:
    TEMP_DIR = Path("temp")
    COOKIES_FILE = "cookies_instagram.txt"

Config.TEMP_DIR.mkdir(exist_ok=True)


class InstagramDownloader:

    def __init__(self, temp_dir: Path):
        self.temp_dir = temp_dir
        self.store = {}        # callback safe storage
        self.cache = {}        # format cache (speed boost)

    # ----------------------------
    # GET FORMATS (FAST + CACHED)
    # ----------------------------
    def get_formats(self, url):

        if url in self.cache:
            return self.cache[url]

        ydl_opts = {
            'quiet': True,
            'noplaylist': True,
        }

        if os.path.exists(Config.COOKIES_FILE):
            ydl_opts['cookiefile'] = Config.COOKIES_FILE

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            formats = []
            for f in info.get("formats", []):
                if f.get("height"):
                    formats.append({
                        "format_id": f["format_id"],
                        "quality": f"{f['height']}p"
                    })

            # remove duplicates
            seen = set()
            unique = []
            for f in formats:
                if f["quality"] not in seen:
                    seen.add(f["quality"])
                    unique.append(f)

            result = unique[:6]

            self.cache[url] = result
            return result

    # ----------------------------
    # DOWNLOAD
    # ----------------------------
    async def download(self, url, format_id):

        ydl_opts = {
            'format': format_id,
            'outtmpl': str(self.temp_dir / '%(title)s.%(ext)s'),
            'quiet': True,
            'merge_output_format': 'mp4',
            'noplaylist': True,
        }

        if os.path.exists(Config.COOKIES_FILE):
            ydl_opts['cookiefile'] = Config.COOKIES_FILE

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._download, ydl_opts, url)

    def _download(self, opts, url):
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file = ydl.prepare_filename(info)

                if os.path.exists(file):
                    return file, info.get("title", "Instagram Video")

        except Exception as e:
            logger.error(f"Download error: {e}")

        return None, None


# ----------------------------
# HANDLERS
# ----------------------------
def setup_ig_handlers(app: Client):

    ig = InstagramDownloader(Config.TEMP_DIR)

    # STEP 1 → GET QUALITIES
    @app.on_message(filters.regex(r"^[/.]ig(\s+https?://\S+)?$"))
    async def ig_handler(client: Client, message: Message):

        parts = message.text.split(maxsplit=1)

        if len(parts) < 2:
            await message.reply_text("❌ Send Instagram link")
            return

        url = parts[1]

        status = await message.reply_text("🔍 Fetching qualities...")

        try:
            formats = ig.get_formats(url)

            if not formats:
                await status.edit("❌ No formats found")
                return

            uid = str(time.time())
            ig.store[uid] = url

            buttons = [
                [InlineKeyboardButton(
                    f["quality"],
                    callback_data=f"ig|{f['format_id']}|{uid}"
                )]
                for f in formats
            ]

            await status.edit(
                "🎥 Select Quality:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        except Exception as e:
            logger.error(e)
            await status.edit("❌ Error fetching qualities")

    # STEP 2 → DOWNLOAD
    @app.on_callback_query(filters.regex(r"^ig\|"))
    async def ig_callback(client: Client, query: CallbackQuery):

        try:
            _, format_id, uid = query.data.split("|")

            url = ig.store.get(uid)

            if not url:
                await query.message.edit("❌ Session expired. Send link again.")
                return

            await query.message.edit("📥 Downloading...")

            file, title = await ig.download(url, format_id)

            if not file:
                await query.message.edit("❌ Download failed")
                return

            try:
                await client.send_video(
                    chat_id=query.message.chat.id,
                    video=file,
                    caption=f"🎬 **{title}**",
                    parse_mode=ParseMode.MARKDOWN
                )

            finally:
                if os.path.exists(file):
                    os.remove(file)

            await query.message.delete()

        except Exception as e:
            logger.error(f"Callback error: {e}")
            await query.message.edit("❌ Something went wrong")
