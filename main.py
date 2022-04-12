import random
from time import time

import telegram
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


def points(update: Update, context: CallbackContext):
    result = server.points(1, 3)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


def main():
    random.seed(time())

    updater = Updater(TOKEN, use_context=True)

    bot = telegram.Bot(token=TOKEN)
    bot.set_webhook(f"https://dfomin.com:443/{TOKEN}")

    updater.start_webhook(listen="127.0.0.1",
                          port=5003,
                          url_path=TOKEN,
                          webhook_url=f"https://dfomin.com:443/{TOKEN}")
    dispatcher: Dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("competitions", competitions))
    dispatcher.add_handler(CommandHandler("points", points))


if __name__ == "__main__":
    main()
