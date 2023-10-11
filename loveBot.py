#!/usr/bin/python

import telebot
from urllib.request import Request, urlopen
import random
import re

def get_compliment():
    link_1 = Request('https://datki.net/komplimenti/devushke/krasivie/', headers={'User-Agent': 'Mozilla/5.0'})
    link_2 = Request('https://datki.net/komplimenti/devushke/krasivie/page/2/', headers={'User-Agent': 'Mozilla/5.0'})
    link_3 = Request('https://datki.net/komplimenti/devushke/krasivie/page/3/', headers={'User-Agent': 'Mozilla/5.0'})
    link_4 = Request('https://datki.net/komplimenti/devushke/krasivie/page/4/', headers={'User-Agent': 'Mozilla/5.0'})
    link_5 = Request('https://datki.net/komplimenti/devushke/krasivie/page/5/', headers={'User-Agent': 'Mozilla/5.0'})
    link_6 = Request('https://datki.net/komplimenti/devushke/krasivie/page/6/', headers={'User-Agent': 'Mozilla/5.0'})
    page = [link_1, link_2, link_3, link_4, link_5, link_6]
    n = random.randint(0, 5)
    print('hi')
    lines = []
    page_num = urlopen(page[n])
    for line in page_num.readlines():
        if line.find(b'div class="entry-header"') == 1:
            lines.append(line)

    todays_line = lines[random.randint(0, len(lines)-1)]
    todays_line = todays_line.decode('utf-8')

    todays_line = todays_line.replace('<div class="entry-header"></div><div class="entry-summary entry-content post-content-', '')
    todays_line = todays_line.replace('</div><div class="entry-footer">', '')
    todays_line = todays_line.replace('<p>', '')
    todays_line = todays_line.replace('<br />', '\n')
    todays_line = todays_line.replace('</p>', '')
    todays_line = re.sub('&#\d\d\d\d;', '', todays_line)
    todays_line = re.sub('\d\d\d\d\d\d">', '', todays_line)
    todays_line = re.sub('\d\d\d\d\d">', '', todays_line)
    
    return todays_line



TOKEN = "
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    keyboard=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=telebot.types.KeyboardButton("*Тык*")
    keyboard.add(button1)
    bot.send_message(m.chat.id, 'Привет, милая!', reply_markup=keyboard)

@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id, 'Напиши /compliment или подожди')

@bot.message_handler(commands=["compliment"])
def compliment(m, res=False):
    bot.send_message(m.chat.id, get_compliment())

@bot.message_handler(commands=["send_message_to_liza"])
def send(m, res=False):
    bot.send_message(1347034777, get_compliment())

@bot.message_handler(content_types=["text"])
def handle_text(m):
    if m.text.strip() == "*Тык*":
        bot.send_message(m.chat.id, get_compliment())

bot.infinity_polling()
