from __future__ import with_statement
from ctypes.wintypes import MSG
from locale import resetlocale
from os.path import commonpath
from re import M
import telebot
import requests
import os
import json, youtube_dl


token = os.environ['TELEGRAM_TOKEN']

# Initialize youtube_dl
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})


bot = telebot.TeleBot(token)
x = bot.get_me()
print(x)



@bot.message_handler(commands=['motivate'])
def send_welc(message):
    quote = requests.request(url='https://api.quotable.io/random', method='get')
    bot.send_message(message.chat.id, quote.json()['content'])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome user")

@bot.message_handler(commands=['ytdl'])
def down(msg):
    args = msg.text.split()[1]
    try:
        with ydl:
            result = ydl.extract_info(
                args,
                download=False
            )

            if 'entries' in result:
                # can be a playlist or a list of videos
                video = result['entries'][0]
            else:
                # Just a video
                video = result

            for i in video['formats']:
                link = '<a href=\"'+ i['url'] + '\">' + 'link' + '</a>'

                if i.get('format_note'):
                    bot.reply_to(msg, 'Quality- ' + i['format_note'] + ':' + link, parse_mode='HTML')

                else:
                    bot.reply_to(msg, link, parse_mode="HTML", display_notification=True)

    except:
        bot.reply_to(msg, 'This can\'t be downloaded by me')

bot.polling()
