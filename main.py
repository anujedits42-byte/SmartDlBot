from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from pyrogram.enums import ParseMode
import os
from config import API_ID, API_HASH, BOT_TOKEN

# Import the handlers
from youtube.youtube import setup_downloader_handler
from pinterest.pinterest import setup_pinterest_handler
from facebook.facebook import setup_dl_handlers
from spotify.spotify import setup_spotify_handler
from instagram.instagram import setup_ig_handlers

# Initialize the bot client
app = Client(
    "app_session",
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

@app.on_message(filters.command(["start"], prefixes=["/", "."]) & filters.private)
async def send_start_message(client, message):
    chat_id = message.chat.id
    full_name = f"{message.from_user.first_name} {message.from_user.last_name}" if message.from_user.last_name else message.from_user.first_name

    # Animation messages
    animation_message = await message.reply_text("<b>Starting Smart Tool ⚙️...</b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.4)  # Use asyncio.sleep instead of sleep
    await animation_message.edit_text("<b>Generating Session Keys Please Wait...</b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.4)  # Use asyncio.sleep instead of sleep
    await animation_message.delete()

    # Main welcome message
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
    "<b>━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
    "<b>🔔 Don't Forget To <a href='https://t.me/anujeditbyak'>Join Here</a> For Updates!</b>"
)
    await message.reply_text(
        start_message,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙️ Help", callback_data="help_menu"),
             InlineKeyboardButton("➕ Add Me", url="https://t.me/social_media_downloader_ak_bot?startgroup=new&admin=post_messages+delete_messages+edit_messages+pin_messages+change_info+invite_users+promote_members")],
            [InlineKeyboardButton("🔄 Updates", url="https://t.me/anujeditbyak"),
             InlineKeyboardButton("ℹ️ About Me", callback_data="about_me")]
        ]),
        disable_web_page_preview=True,
    )

@app.on_callback_query(filters.regex("help_menu"))
async def help_menu_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.answer()   # ✅ HERE

    help_message = (
        "<b>🎥 Social Media and Music Downloader</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>USAGE:</b>\n"
        "Download videos and tracks from popular platforms using these commands:\n\n"
        "➢ <b>/fb [Video URL]</b> - Download a Facebook video.\n"
        "   - Example: <code>/fb https://www.facebook.com/share/v/18VH1yNXoq/</code> (Downloads the specified Facebook video)\n"
        "   - Note: Private Facebook videos cannot be downloaded.\n\n"
        "➢ <b>/pin [Video URL]</b> - Download a Pinterest video.\n"
        "   - Example: <code>/pin https://pin.it/6GoDMRwmE</code> (Downloads the specified Pinterest video)\n\n"
        "➢ <b>/ig [Video URL]</b> - Download an Instagram video/reel. \n"
        "    - Example: /ig https://www.instagram.com/reel/XXXXXXX/ (Downloads the specified Instagram video)\n\n"
        "   - Note: 18+ Instagram Reels cannot be downloaded.\n\n"
        "➢ <b>/sp [Track URL]</b> - Download a Spotify track.\n"
        "   - Example: <code>/sp https://open.spotify.com/track/7ouBSPZKQpm7zQz2leJXta</code> (Downloads the specified Spotify track)\n\n"
        "➢ <b>/yt [Video URL]</b> - Download a YouTube video.\n"
        "   - Example: <code>/yt https://youtu.be/In8bfGnXavw</code> (Downloads the specified YouTube video)\n\n"
        "➢ <b>/song [Video URL]</b> - Download a YouTube video as an MP3 file.\n"
        "   - Example: <code>/song https://youtu.be/In8bfGnXavw</code> (Converts and downloads the video as MP3)\n\n"
        ">NOTE:\n"
        "1️⃣ Provide a valid public URL for each platform to download successfully.\n\n"
        ">🔔 For Bot Update News: <a href='https://t.me/anujeditbyak'>Join Now</a>"
    )

    await callback_query.message.edit_text(
        help_message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="start_menu")]
        ])
    )

@app.on_callback_query(filters.regex("about_me"))
async def about_me_callback(client: Client, callback_query: CallbackQuery):
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

    await callback_query.message.edit_text(
        about_message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="start_menu")]
        ])
    )

@app.on_callback_query(filters.regex("start_menu"))
async def start_menu_callback(client: Client, callback_query: CallbackQuery):
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name}" if callback_query.from_user.last_name else callback_query.from_user.first_name

    start_message = (
        f"<b>Hi {full_name}! Welcome To This Bot...</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b><a href='tg://user?id=7892805795'>Smart Tool ⚙️</a></b>: The ultimate toolkit on Telegram, offering Facebook,YouTube,Pinterest,Spotify Downloader. Simplify your tasks with ease!\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>Don't Forget To <a href='https://t.me/anujeditbyak'>Join Here</a> For Updates!</b>"
    )

    await callback_query.message.edit_text(
        start_message,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙️ Help", callback_data="help_menu"),
             InlineKeyboardButton("➕ Add Me", url="https://t.me/social_media_downloader_ak_bot?startgroup=new&admin=post_messages+delete_messages+edit_messages+pin_messages+change_info+invite_users+promote_members")],
            [InlineKeyboardButton("🔄 Updates", url="https://t.me/anujeditbyak"),
             InlineKeyboardButton("ℹ️ About Me", callback_data="about_me")]
        ]),
        disable_web_page_preview=True,
    )

print("Bot Successfully Started! 💥")

app.run()
