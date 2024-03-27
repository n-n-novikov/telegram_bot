#!/usr/bin/python

import telebot
import random
import re
import schedule
import time
import threading
import requests
import json

#----------------------------------------- CONST
liz = 1
admin = 0
TOKEN = ""
bot = telebot.TeleBot(TOKEN)
CAT_URL = "https://api.thecatapi.com/v1/images/search"
#-----------------------------------------

#----------------------------------------- поменяю на sql ради интереса
file = open('comps.txt')
comps = []
for line in file.readlines():
    comps.append(line)
#-----------------------------------------

#----------------------------------------- функции для многопоточности
def polling():
    bot.infinity_polling()
    time.sleep(5)

def scheduling():
    while True:
        schedule.run_pending()
        time.sleep(30)
#-----------------------------------------

#----------------------------------------- функции по сути
def get_compliment():
    todays_line = comps[random.randint(0, len(comps)-1)]
    todays_line = todays_line.replace('\\n ', '\n')
    return todays_line

def get_cat():
    global CAT_URL
    responce = requests.get(CAT_URL)
    photo_url = json.loads(responce.text[1:-1])['url']
    photo = requests.get(photo_url)
    return photo.content

def morning(what):
    if what == 'comp':
        bot.send_message(liz, get_compliment())
    elif what == 'cat':
        bot.send_photo(liz, get_cat())

schedule.every().day.at('10:30', 'Europe/Moscow').do(morning, what='comp')
schedule.every().day.at('17:00', 'Europe/Moscow').do(morning, what='comp')
schedule.every(2).hours.at(':15').do(morning, what='cat')
#-----------------------------------------

#----------------------------------------- обработка команд
@bot.message_handler(commands=["start"])
def start(m, res=False):
    keyboard=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=telebot.types.KeyboardButton("*Тык*")
    button2=telebot.types.KeyboardButton("*Кыт*")
    keyboard.add(button1)
    keyboard.add(button2)

    bot.send_message(m.chat.id, 'Привет, милая!', reply_markup=keyboard)

@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id, 'Напиши /compliment или подожди')

@bot.message_handler(commands=["compliment"])
def compliment(m, res=False):
    bot.send_message(m.chat.id, get_compliment())

@bot.message_handler(commands=["send_message_to_liza"])
def send(m, res=False):
    bot.send_message(liz, get_compliment())

@bot.message_handler(content_types=["text"])
def handle_text(m):
    if m.text.strip() == "*Тык*":
        bot.send_message(m.chat.id, get_compliment())
    elif m.text.strip() == "*Кыт*":
        bot.send_photo(m.chat.id, get_cat())
    else:
        bot.send_message(m.chat.id, 'Таких букав я уже не понимаю(')
#-----------------------------------------

# thread_poll = threading.Thread(target = polling)
# thread_poll.start()           какая-то новая ошибка, поэтому поллинг в поток не заносим

thread_sched = threading.Thread(target = scheduling)
thread_sched.start()
bot.infinity_polling()






# ---------------LEGACY--------------------------------------------------------------------------------------------------------------------
# Так как сайт установил DDOS-Guard - запросы к нему иногда блокируются, поэтому все сделал ручками с помощью скрипта. Зато так стабильней будет.

# from urllib.request import Request, urlopen

# def get_compliment():
#     link_1 = Request('https://datki.net/komplimenti/devushke/krasivie/', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.962 YaBrowser/23.9.1.962 Yowser/2.5 Safari/537.36'})
#     link_2 = Request('https://datki.net/komplimenti/devushke/krasivie/page/2/', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.962 YaBrowser/23.9.1.962 Yowser/2.5 Safari/537.36'})
#     link_3 = Request('https://datki.net/komplimenti/devushke/krasivie/page/3/', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.962 YaBrowser/23.9.1.962 Yowser/2.5 Safari/537.36'})
#     link_4 = Request('https://datki.net/komplimenti/devushke/krasivie/page/4/', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.962 YaBrowser/23.9.1.962 Yowser/2.5 Safari/537.36'})
#     link_5 = Request('https://datki.net/komplimenti/devushke/krasivie/page/5/', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.962 YaBrowser/23.9.1.962 Yowser/2.5 Safari/537.36'})
#     link_6 = Request('https://datki.net/komplimenti/devushke/krasivie/page/6/', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.962 YaBrowser/23.9.1.962 Yowser/2.5 Safari/537.36'})
#     page = [link_1, link_2, link_3, link_4, link_5, link_6]
#     n = random.randint(0, 5)
#     print('hi')
#     lines = []
#     page_num = urlopen(page[n])
#     print(page_num.readline())
    
#     for line in page_num.readlines():
#         if line.find(b'div class="entry-header"') == 1:
#             lines.append(line)
#         print(line)
#     print('------------------------------------------------------------------',len(lines))
#     todays_line = lines[random.randint(0, len(lines)-1)]
#     todays_line = todays_line.decode('utf-8')

#     todays_line = todays_line.replace('<div class="entry-header"></div><div class="entry-summary entry-content post-content-', '')
#     todays_line = todays_line.replace('</div><div class="entry-footer">', '')
#     todays_line = todays_line.replace('<p>', '')
#     todays_line = todays_line.replace('<br />', '\n')
#     todays_line = todays_line.replace('</p>', '')
#     todays_line = re.sub('&#\d\d\d\d;', '', todays_line)
#     todays_line = re.sub('\d\d\d\d\d\d">', '', todays_line)
#     todays_line = re.sub('\d\d\d\d\d">', '', todays_line)
    
#     return todays_line
