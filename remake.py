#!/usr/bin/python

import telebot
from urllib.request import Request, urlopen
import random
import re

page_num = open('comps_raw.txt')
new_f = open ('comps.txt', 'a')

lines = []
for line in page_num.readlines():
    if line.find('div class="entry-summary entry-content') == 1:
        # print(line)
        lines.append(line)


for line in lines:
    todays_line = line

    todays_line = todays_line.replace('<div class="entry-summary entry-content post-content-', '')
    todays_line = todays_line.replace('</div></div><div class="d-flex justify-content-center temp-padding">', '')
    todays_line = todays_line.replace('<p>', '')
    todays_line = todays_line.replace('<br />', '\\n')
    todays_line = todays_line.replace('</p>', '')
    todays_line = re.sub('&#\d\d\d\d;', '', todays_line)
    todays_line = re.sub('&#\d\d\d;', '', todays_line)
    todays_line = re.sub('\d\d\d\d\d\d">', '', todays_line)
    todays_line = re.sub('\d\d\d\d\d">', '', todays_line)
    print(todays_line)
    new_f.write(todays_line)

new_f.close()
page_num.close()
