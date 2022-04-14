import random
from time import time

import telegram
from telegram import Update
from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackContext

import server
from private import TOKEN


def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name

    server.create_user(user_id, user_name)


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋🏻")


def competitions(update: Update, context: CallbackContext):
    result = server.competitions()
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


def create_competition(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    name = " ".join(update.message.text.split()[1:]).strip()
    competition_id = server.create_competition(name)

    server.join(user_id, competition_id)

    context.bot.send_message(chat_id=update.effective_chat.id, text=competition_id)


def join(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    parts = update.message.text.split()
    if len(parts) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="/join <competition_id>")
        return

    try:
        competition_id = int(parts[1])
        server.join(user_id, competition_id)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="/join <competition_id>")
        return


def add_match(update: Update, context: CallbackContext):
    parts = update.message.text.split()
    if len(parts) != 3:
        context.bot.send_message(chat_id=update.effective_chat.id, text="/add_match <competition_id> <team1>-<team2>")
        return

    competition_id = int(parts[1])
    name = parts[2]
    if len(name.split("-")) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="/add_match <competition_id> <team1>-<team2>")
        return

    server.add_match(competition_id, name)


def points(update: Update, context: CallbackContext):
    competition_id, points_id = map(int, update.message.text.split()[1:])
    result = ""
    for name, value in server.points(competition_id, points_id).items():
        result += f"{name}: {value}\n"
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
    dispatcher.add_handler(CommandHandler("create_competition", create_competition))

    dispatcher.add_handler(CommandHandler("join", join))

    dispatcher.add_handler(CommandHandler("add_match", add_match))

    dispatcher.add_handler(CommandHandler("points", points))


if __name__ == "__main__":
    main()
