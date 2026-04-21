import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaDocument
from pyrogram.enums import ParseMode
from config import ADMIN_IDS  # Import ADMIN_IDS

def setup_logs_handler(app: Client):
    """Sets up the logs handler to send logs from botlog.txt only."""
    
    @app.on_message(filters.command(["dump", "logs"], prefixes=["/", "."]) & (filters.private | filters.group))
    async def logs_command(client, message):
        """Sends logs from botlog.txt to admins only."""

        # Check if the user is an admin
        if message.from_user.id not in ADMIN_IDS:
            await client.send_message(
                chat_id=message.chat.id, 
                text="**❌ You do not have permission to use this command.**", 
                parse_mode=ParseMode.MARKDOWN
            )
            return

        # Send loading message
        loading_msg = await client.send_message(
            chat_id=message.chat.id, 
            text="🚀 **Fetching Logs Database🔥**", 
            parse_mode=ParseMode.MARKDOWN
        )

        logs = "No logs available yet."

        # Read the logs from botlog.txt if it exists
        if os.path.exists("botlog.txt"):
            with open("botlog.txt", "r", encoding="utf-8") as f:
                logs = f.read().strip()

        # If logs are too long, send as a text file
        if len(logs) > 4000:
            log_file_path = "botlog.txt"
            await client.send_document(
                chat_id=message.chat.id,
                document=log_file_path,
                caption="📜 **Here are the latest logs:**",
                parse_mode=ParseMode.MARKDOWN
            )
            await loading_msg.delete()
        else:
            # Format logs as plain text
            logs_formatted = f"📜 Latest Logs:\n\n{logs}"

            # Create an inline "Close" button
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("❌ Close", callback_data="close_logs")]]
            )

            # Edit the loading message with logs
            await loading_msg.edit_text(logs_formatted, parse_mode=ParseMode.DISABLED, reply_markup=keyboard)

    @app.on_callback_query(filters.regex("close_logs"))
    async def close_logs(client: Client, query: CallbackQuery):
        """Deletes the log message when the 'Close' button is clicked."""
        await query.message.delete()
