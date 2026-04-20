import os
import logging
import time
from pathlib import Path
from typing import Optional
import yt_dlp
import asyncio

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

    def get_formats(self, url):
        ydl_opts = {
            'quiet': True,
            'cookiefile': Config.COOKIES_FILE if os.path.exists(Config.COOKIES_FILE) else None
        }

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

            return unique[:6]  # limit buttons

    async def download(self, url, format_id):

        ydl_opts = {
            'format': format_id,
            'outtmpl': str(self.temp_dir / '%(title)s.%(ext)s'),
            'cookiefile': Config.COOKIES_FILE if os.path.exists(Config.COOKIES_FILE) else None,
            'quiet': True,
            'merge_output_format': 'mp4'
        }

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._download, ydl_opts, url)

    def _download(self, opts, url):
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)

            if os.path.exists(file):
                return file, info.get("title", "Instagram Video")

        return None, None


def setup_ig_handlers(app: Client):

    ig = InstagramDownloader(Config.TEMP_DIR)

    # STEP 1 → Send quality buttons
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

            buttons = [
                [InlineKeyboardButton(f["quality"], callback_data=f"ig|{f['format_id']}|{url}")]
                for f in formats
            ]

            await status.edit(
                "🎥 Select Quality:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        except Exception as e:
            logger.error(e)
            await status.edit("❌ Error fetching qualities")

    # STEP 2 → Handle button click
    @app.on_callback_query(filters.regex(r"^ig\|"))
    async def ig_callback(client: Client, query: CallbackQuery):

        _, format_id, url = query.data.split("|")

        await query.message.edit("📥 Downloading...")

        file, title = await ig.download(url, format_id)

        if not file:
            await query.message.edit("❌ Download failed")
            return

        await client.send_video(
            chat_id=query.message.chat.id,
            video=file,
            caption=f"🎬 **{title}**",
            parse_mode=ParseMode.MARKDOWN
        )

        os.remove(file)
        await query.message.delete()
