import telebot

def init_bot(api_key: str):
    bot = telebot.TeleBot(token=api_key)
    return bot
