from pyrogram import Client, filters, errors
from pyrogram.types import InlineKeyboardButton, InlineQueryResult, CallbackQuery, ChatPermissions, ChatPrivileges, InputMediaAudio



api_id = '27210213'
api_hash = 'c43dff8fceda05ca737d4cee163136de'
bot_token ="7596494471:AAGvgm9tnSYWouJV6Yyi6lnjmpoKHbLsA3Y"


bot = Client( 'bot' , api_id= api_id, api_hash=api_hash, bot_token= bot_token)

@bot.on_message(filters.command('start') & filters.private)
def start(bot, message):
    bot.send_message(message.chat.id, f""" <b>HELLO {message.from_user.mention} </b>""", disable_web_page_preview = True)

print("Bot started")
bot.run()