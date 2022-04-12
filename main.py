import random
from time import time

from telegram import Update
from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackContext

import server
from private import TOKEN


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋🏻")


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋🏻")


def competitions(update: Update, context: CallbackContext):
    result = server.competitions()
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


def main():
    random.seed(time())

    updater = Updater(TOKEN, use_context=True)

    updater.start_webhook(listen="127.0.0.1",
                          port=5003,
                          url_path=TOKEN,
                          webhook_url=f"https://dfomin.com:443/{TOKEN}")
    dispatcher: Dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("competitions", competitions))


if __name__ == "__main__":
    main()
