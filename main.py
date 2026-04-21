from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
import asyncio
import threading
from flask import Flask
import os

from config import API_ID, API_HASH, BOT_TOKEN

# Import handlers
from youtube.youtube import setup_downloader_handler
from pinterest.pinterest import setup_pinterest_handler
from facebook.facebook import setup_dl_handlers
from spotify.spotify import setup_spotify_handler
from instagram.instagram import setup_ig_handlers


# ------------------- FLASK SERVER -------------------

web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is running!"

def run_web():
    web_app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False,
        use_reloader=False   # 🔥 ye hi fix hai
    )


# ------------------- PYROGRAM BOT -------------------

app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN 
)

# Setup handlers
setup_downloader_handler(app)
setup_pinterest_handler(app)
setup_dl_handlers(app)
setup_spotify_handler(app)
setup_ig_handlers(app)


# ------------------- START -------------------

@app.on_message(filters.command(["start"]) & filters.private)
async def start(client, message):
    full_name = f"{message.from_user.first_name} {message.from_user.last_name}" if message.from_user.last_name else message.from_user.first_name

    animation = await message.reply_text("<b>Starting Smart Tool ⚙️...</b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.4)
    await animation.edit_text("<b>Generating Session Keys Please Wait...</b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.4)
    await animation.delete()

    start_message = (
        f"<b>👋🏻 Hello {full_name}!</b>\n\n"
        "<b>📥 I can help you download videos and images from:</b>\n\n"
        "🌐 YouTube\n"
        "📸 Instagram\n"
        "🎵 TikTok\n"
        "📌 Pinterest\n"
        "👻 Snapchat\n"
        "🎬 Likee\n"
        "🌍 VK\n"
        "📘 Facebook\n"
        "🧵 Threads\n"
        "🎧 Music\n\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        "• <b>Just send me a link</b> and I will download it instantly ⚡\n\n"
        "<b>💡 Note:</b> The bot also works in groups.\n"
        "If you want to use it in a group, press the button below 👇\n\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>🔔 Don't Forget To <a href='https://t.me/anujeditbyak'>Join Here</a> For Updates!</b>"
    )

    await message.reply_photo(
        photo="https://h.uguu.se/vCWUTJSx.jpg",
        caption=start_message,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚙️ Help", callback_data="help_menu"),
                InlineKeyboardButton("➕ Add Me", url="https://t.me/social_media_downloader_ak_bot?startgroup=new")
            ],
            [
                InlineKeyboardButton("🔄 Updates", url="https://t.me/anujeditbyak"),
                InlineKeyboardButton("ℹ️ About Me", callback_data="about_me")
            ]
        ])
    )


# ------------------- HELP COMMAND -------------------

@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    text = (
        "<b>🎥 Downloader Help</b>\n\n"
        "/fb - Facebook\n"
        "/pin - Pinterest\n"
        "/ig - Instagram\n"
        "/sp - Spotify\n"
        "/yt - YouTube\n"
        "/song - MP3"
    )

    await message.reply_text(text, parse_mode=ParseMode.HTML)

# ------------------- ABOUT COMMAND -------------------

@app.on_message(filters.command("about"))
async def about_cmd(client, message):
    text = (
        "<b>Smart Tool ⚙️</b>\n"
        "Version: 3.0\n\n"
        "Developer: @anujedits76\n"
        "Library: Pyrogram"
    )

    await message.reply_text(text, parse_mode=ParseMode.HTML)

# ------------------- BUTTON HELP -------------------

@app.on_callback_query(filters.regex("help_menu"))
async def help_menu(client, query: CallbackQuery):
    await query.answer()

    text = (
        "<b>🎥 Downloader Help</b>\n\n"
        "/fb - Facebook\n"
        "/pin - Pinterest\n"
        "/ig - Instagram\n"
        "/sp - Spotify\n"
        "/yt - YouTube\n"
        "/song - MP3"
    )

    await query.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="start_menu")]
        ])
    )

# ------------------- BUTTON ABOUT -------------------

@app.on_callback_query(filters.regex("about_me"))
async def about_menu(client, query: CallbackQuery):
    await query.answer()

    text = (
        "<b>Smart Tool ⚙️</b>\n"
        "Version: 3.0\n\n"
        "Developer: @anujedits76\n"
        "Library: Pyrogram"
    )

    await query.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="start_menu")]
        ])
    )

# ------------------- BACK -------------------

@app.on_callback_query(filters.regex("start_menu"))
async def back(client, query: CallbackQuery):
    await query.answer()

    await query.message.edit_text(
        "<b>Send me any link to download 🚀</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚙️ Help", callback_data="help_menu"),
                InlineKeyboardButton("ℹ️ About", callback_data="about_me")
            ]
        ])
    )

# ------------------- RUN -------------------

print("Bot Started 💥")

threading.Thread(target=run_web, daemon=True).start()
app.run()
