from pyrogram import Client, filters, errors
from pyrogram.types import InlineKeyboardButton, InlineQueryResult, CallbackQuery, ChatPermissions, ChatPrivileges, InputMediaAudio , InlineKeyboardMarkup



api_id = '27210213'
api_hash = 'c43dff8fceda05ca737d4cee163136de'
bot_token ="7596494471:AAGvgm9tnSYWouJV6Yyi6lnjmpoKHbLsA3Y"


app = Client( 'bot' , api_id= api_id, api_hash=api_hash, bot_token= bot_token)


# welcome the user

@app.on_message(filters.command('start') & filters.private)
def start(bot, message):
    bot.send_message(message.chat.id, f""" <b>Hi!  {message.from_user.mention},
                     
I am a travel ticket Bot 🌎
                     
You can search cheapest flight for your destination ✈️
                     
Let's start by clicking /book
                     </b>""", disable_web_page_preview = True )



@app.on_message(filters.command('book'))
def book(app,message):
    button = [
        [InlineKeyboardButton('✈️ Book Cheapest Flight', callback_data="b_flight")],
        [InlineKeyboardButton('🛠 Comming soon', callback_data="c_soon")]
    ]
    message.reply_text(
        text="**Please Choose a commad listed below**",
        reply_markup =InlineKeyboardMarkup(button)
    )

@app.on_callback_query()
def callback_data(bot, x: CallbackQuery):
    if 'b_flight' in x.data:
        text = """
**Booking Flight✈️

We will be bringing this Feature soon 

with more exciting commands

**
"""
        bot.edit_message_text(
            chat_id=x.message.chat.id,
            text=text,
            message_id=x.message.id,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Coming soon', callback_data='coming')]])
        )

try:
    print("App initiated")
    app.run()
except Exception as e:
    print("Their was an error while initializing the app")