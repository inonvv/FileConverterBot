from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os
from bot_commands.commands import start_command, handle_message, handle_extension_choice

TELEGRAM_BOT_TOKEN = os.getenv("BOT_KEY")
TELEGRAM_BOT_NAME = os.getenv("BOT_NAME")

if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    app.add_handler(CallbackQueryHandler(handle_extension_choice))
    app.run_polling(poll_interval=3)
