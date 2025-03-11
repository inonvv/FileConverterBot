from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from src.file_converters.supported_conversions import supported_conversions
import os
from dotenv import load_dotenv
from src.Logs.logger import Logger

from telegram.error import TelegramError
from telegram.constants import FileSizeLimit

load_dotenv()


from src.file_converters.converter_factory import ConverterFactory

# Dictionary to store user file paths temporarily
user_files = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Drag your file to convert it!")


def build_log(message, extra_data=None):
    full_data = {"message": message}
    if extra_data:
        full_data.update(extra_data)
    return full_data


def log_error(message, extra_data=None):
    logger = Logger()
    logger.log_error(build_log(message, extra_data))


def log_success(message, extra_data=None):
    logger = Logger()
    logger.log_success(build_log(message, extra_data))


def log_info(message, extra_data=None):
    logger = Logger()
    logger.log_info(build_log(message, extra_data))


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_info("new file upload request")
    # Determine file type and get file details
    if update.message.document:
        log_info("the file is document")
        file_obj = update.message.document
        file_name = file_obj.file_name
    elif update.message.photo:
        log_info("the file is photo")
        file_obj = update.message.photo[-1]  # Get the largest photo size
        file_name = f"photo_{update.message.date.strftime('%Y%m%d_%H%M%S')}.jpg"
    elif update.message.sticker and update.message.sticker.is_animated is False:
        log_info("the file is an image")
        file_obj = update.message.sticker
        file_name = f"image_{update.message.date.strftime('%Y%m%d_%H%M%S')}.webp"
    else:
        await update.message.reply_text("Please send a document or photo to convert.")
        return

    file_id = file_obj.file_id
    file_size = file_obj.file_size

    # Log file size for debugging
    log_info("file details", {"file_id": file_id, "file_size_mb": file_size / (1024 * 1024)})

    # Check file size before attempting download
    if file_size > FileSizeLimit.FILESIZE_DOWNLOAD:
        log_error("file too large", {"file_id": file_id, "file_size_mb": file_size / (1024 * 1024)})
        await update.message.reply_text(
            f"File is too large. Maximum size is {FileSizeLimit.FILESIZE_DOWNLOAD / (1024 * 1024):.1f}MB. "
            "Please upload a smaller file."
        )
        return

    try:
        file = await context.bot.get_file(file_id)
    except TelegramError as error:
        error_message = str(error)
        log_error("failed to get the file", {
            "error_message": error_message,
            "file_size_mb": file_size / (1024 * 1024), "file_id": file_id
        })
        await update.message.reply_text(
            f"Failed to upload file\n"
            "Please try a smaller file or contact support."
        )
        return

    original_file_path = f"./{file_name}"
    log_info("try to save file", {"file path": original_file_path, "file_id": file_id})

    try:
        await file.download_to_drive(original_file_path)
        log_success("file saved successfully", {"file path": original_file_path, "file_id": file_id})
        # Store the file path for the user
        user_files[update.effective_user.id] = original_file_path
    except Exception as error:
        log_error("failed to save", {
            "file path": original_file_path, "file_id": file_id,
            "error_message": str(error)
        })
        await update.message.reply_text("Failed to save file. Please try again.")
        return
    file_name = os.path.basename(original_file_path)
    name, file_extension = os.path.splitext(file_name)
    # Generate inline keyboard with extension options
    keyboard = [
        [InlineKeyboardButton(ext, callback_data=ext) for ext in supported_conversions[file_extension].keys()]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Ask the user to choose an extension
    await update.message.reply_text(
        "Choose the extension to convert your file to:",
        reply_markup=reply_markup
    )


async def handle_extension_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_info("file convert request")
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    user_id = query.from_user.id
    chosen_extension = query.data

    # Retrieve the user's original file
    log_info("trying to retrieve user original file", {"user id": user_id})
    original_file_path = user_files.get(user_id)

    if not original_file_path:
        log_error("failed to retrieve the file path from the user id", {"user id": user_id})
        await query.edit_message_text("No file found for conversion. Please send a file first.")
        return

    log_success("successfully retrieve the file", {"file path": original_file_path})

    file_name = os.path.basename(original_file_path)
    name, ext = os.path.splitext(file_name)
    new_file_path = f"./{name}{chosen_extension.lower()}"  # New file with the chosen extension
    log_info("try to convert file", {"original_file_path": original_file_path, "new_file_path": new_file_path})
    # Convert the file
    try:
        ConverterFactory.convert_file(original_file_path, chosen_extension)
        log_success("file converted", {"original_file_path": original_file_path, "new_file_path": new_file_path})

        # Send the new file back to the user
        log_info("sending the document to bot")
        await context.bot.send_document(chat_id=query.message.chat.id, document=open(new_file_path, 'rb'))

        # Cleanup files
        os.remove(original_file_path)
        os.remove(new_file_path)

        # Confirmation message
        await query.edit_message_text(f"File has been converted to {chosen_extension} and returned!")
        log_info("sending success message to user")
    except Exception as e:
        print(e)
        await query.edit_message_text(f"An error occurred during conversion: ")
        log_error("failed with converting the file",
                  {"original_file_path": original_file_path, "new_file_path": new_file_path, "error": str(e)})
