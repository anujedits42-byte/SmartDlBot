import os
import asyncio
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from config import API_ID, API_HASH, BOT_TOKEN
from utils import LOGGER

# Import handlers
from youtube.youtube import setup_downloader_handler
from pinterest.pinterest import setup_pinterest_handler
from facebook.facebook import setup_dl_handlers
from spotify.spotify import setup_spotify_handler
from instagram.instagram import setup_ig_handlers
from tiktok.tiktok import setup_tt_handler
from adminpanel.restart.restart import setup_restart_handler
from adminpanel.admin.admin import setup_admin_handler
from adminpanel.logs.logs import setup_logs_handler


# ------------------- FLASK SERVER -------------------

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Smart Tool Bot is Running 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )

# Run Flask in background (daemon thread)
Thread(target=run_flask, daemon=True).start()

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
setup_restart_handler(app)
setup_admin_handler(app)
setup_logs_handler(app)
setup_tt_handler(app)


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
    help_message = (
    "<b>🎥 Social Media and Music Downloader</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "<b>USAGE:</b>\n"
    "Download videos and tracks from popular platforms using these commands:\n\n"

    "➢ <b>/fb [Video URL]</b> - Download a Facebook video.\n"
    "   - Example: <code>/fb https://www.facebook.com/share/v/18VH1yNXoq/</code>\n"
    "   - Note: Private Facebook videos cannot be downloaded.\n\n"

    "➢ <b>/pin [Video URL]</b> - Download a Pinterest video.\n"
    "   - Example: <code>/pin https://pin.it/6GoDMRwmE</code>\n\n"

    "➢ <b>/ig [Video URL]</b> - Download Instagram Reels / Posts.\n"
    "   - Example: <code>/ig https://www.instagram.com/reel/xyz/</code>\n"
    "   - Note: Private or 18+ content cannot be downloaded.\n\n"

    "➢ <b>/tt [Video URL]</b> - Download a TikTok video.\n"
    "   - Example: <code>/tt https://www.tiktok.com/@username/video/1234567890123456789</code>\n"

    "➢ <b>/sp [Track URL]</b> - Download a Spotify track.\n"
    "   - Example: <code>/sp https://open.spotify.com/track/7ouBSPZKQpm7zQz2leJXta</code>\n\n"

    "➢ <b>/yt [Video URL]</b> - Download a YouTube video.\n"
    "   - Example: <code>/yt https://youtu.be/In8bfGnXavw</code>\n\n"

    "➢ <b>/song [Video URL]</b> - Download YouTube video as MP3.\n"
    "   - Example: <code>/song https://youtu.be/In8bfGnXavw</code>\n\n"

    ">NOTE:\n"
    "1️⃣ Provide a valid public URL for each platform.\n\n"

    ">🔔 For Bot Update News: <a href='https://t.me/anujeditbyak'>Join Now</a>"
)

    await message.reply_text(help_message, parse_mode=ParseMode.HTML)

# ------------------- ABOUT COMMAND -------------------

@app.on_message(filters.command("about"))
async def about_cmd(client, message):
    about_message = (
        "<b>Name:</b> Smart Tool ⚙️\n"
        "<b>Version:</b> 3.0 (Beta Testing) 🛠\n\n"
        "<b>Development Team:</b>\n"
        "- <b>Creator:</b> <a href='https://t.me/anujedits76'>𝐀𝐧𝐮𝐣 👨‍💻</a>\n"
        "<b>Technical Stack:</b>\n"
        "- <b>Language:</b> Python 🐍\n"
        "- <b>Libraries:</b> Aiogram, Pyrogram And Telethon 📚\n"
        "- <b>Database:</b> MongoDB Database 🗄\n"
        "- <b>Hosting:</b> Hostinger VPS 🌐\n\n"
        "<b>About:</b> Smart Tool ⚙️ The ultimate toolkit on Telegram, offering Facebook,YouTube,Pinterest,Spotify Downloader. Simplify your tasks with ease!\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/anujeditbyak'>Join Now</a>"
    )

    await message.reply_text(about_message, parse_mode=ParseMode.HTML)

# ------------------- BUTTON HELP -------------------

@app.on_callback_query(filters.regex("help_menu"))
async def help_menu(client, query: CallbackQuery):
    await query.answer()

    help_message = (
    "<b>🎥 Social Media and Music Downloader</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "<b>USAGE:</b>\n"
    "Download videos and tracks from popular platforms using these commands:\n\n"

    "➢ <b>/fb [Video URL]</b> - Download a Facebook video.\n"
    "   - Example: <code>/fb https://www.facebook.com/share/v/18VH1yNXoq/</code>\n"
    "   - Note: Private Facebook videos cannot be downloaded.\n\n"

    "➢ <b>/pin [Video URL]</b> - Download a Pinterest video.\n"
    "   - Example: <code>/pin https://pin.it/6GoDMRwmE</code>\n\n"

    "➢ <b>/ig [Video URL]</b> - Download Instagram Reels / Posts.\n"
    "   - Example: <code>/ig https://www.instagram.com/reel/xyz/</code>\n"
    "   - Note: Private or 18+ content cannot be downloaded.\n\n"

    "➢ <b>/tt [Video URL]</b> - Download a TikTok video.\n"
    "   - Example: <code>/tt https://www.tiktok.com/@username/video/1234567890123456789</code>\n"   

    "➢ <b>/sp [Track URL]</b> - Download a Spotify track.\n"
    "   - Example: <code>/sp https://open.spotify.com/track/7ouBSPZKQpm7zQz2leJXta</code>\n\n"

    "➢ <b>/yt [Video URL]</b> - Download a YouTube video.\n"
    "   - Example: <code>/yt https://youtu.be/In8bfGnXavw</code>\n\n"

    "➢ <b>/song [Video URL]</b> - Download YouTube video as MP3.\n"
    "   - Example: <code>/song https://youtu.be/In8bfGnXavw</code>\n\n"

    ">NOTE:\n"
    "1️⃣ Provide a valid public URL for each platform.\n\n"

    ">🔔 For Bot Update News: <a href='https://t.me/anujeditbyak'>Join Now</a>"
)

    await query.message.edit_text(
    help_message,
    parse_mode=ParseMode.HTML,
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="start_menu")]
    ])
)
    
# ------------------- BUTTON ABOUT -------------------

@app.on_callback_query(filters.regex("about_me"))
async def about_menu(client, query: CallbackQuery):
    await query.answer()

    about_message = (
        "<b>Name:</b> Smart Tool ⚙️\n"
        "<b>Version:</b> 3.0 (Beta Testing) 🛠\n\n"
        "<b>Development Team:</b>\n"
        "- <b>Creator:</b> <a href='https://t.me/anujedits76'>𝐀𝐧𝐮𝐣 👨‍💻</a>\n"
        "<b>Technical Stack:</b>\n"
        "- <b>Language:</b> Python 🐍\n"
        "- <b>Libraries:</b> Aiogram, Pyrogram And Telethon 📚\n"
        "- <b>Database:</b> MongoDB Database 🗄\n"
        "- <b>Hosting:</b> Hostinger VPS 🌐\n\n"
        "<b>About:</b> Smart Tool ⚙️ The ultimate toolkit on Telegram, offering Facebook,YouTube,Pinterest,Spotify Downloader. Simplify your tasks with ease!\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/anujeditbyak'>Join Now</a>"
    )

    await query.message.edit_text(
    about_message,
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
    ]),
    disable_web_page_preview=True,
)

# Final confirmation that the bot has started
print("✅ Bot Successfully Started and Flask is running on Heroku.")
app.run()
