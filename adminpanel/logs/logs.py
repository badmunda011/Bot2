import logging
import io
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from config import ADMIN_IDS  # Make sure to import your ADMIN_IDS

# Create a StringIO buffer to store logs
log_buffer = io.StringIO()

def setup_logs_handler(app: Client):
    """Sets up logging to capture console output."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a StreamHandler to capture logs in a buffer
    stream_handler = logging.StreamHandler(log_buffer)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)

    # Remove old handlers to prevent duplicate logs
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.addHandler(stream_handler)

    logging.info(" Bot Successfully Started! 💥")

    @app.on_message(filters.command("logs") & (filters.private | filters.group))
    async def logs_command(client, message):
        """Sends a loading message first, then edits it with logs, only for admins."""

        # Check if the user is an admin
        if message.from_user.id not in ADMIN_IDS:
            await message.reply_text("❌ You do not have permission to use this command.")
            return

        # Send loading message
        loading_msg = await message.reply_text("🚀 **Fetching Logs Database🔥**", parse_mode=ParseMode.MARKDOWN)

        # Read the current logs from the buffer
        log_buffer.seek(0)  # Move to the start of the buffer
        logs = log_buffer.read().strip()  # Read logs

        if not logs:
            logs = "No logs available yet."

        # Format logs as normal text (no bold, no monospace)
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