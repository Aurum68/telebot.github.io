from datetime import datetime
import sqlite3
from threading import Thread
import logging
from os import getenv

import vk_api
import telebot


CHAT_ID = -1001895882875
TELEGRAM_BOT_TOKEN = getenv("TBB__TELEGRAM_BOT_TOKEN")
VK_BOT_TOKEN = getenv("TBB__VK_BOT_TOKEN")

nums = {"1": "01", "2": "02", "3": "03", "4": "04", "5": "05", "6": "06", "7": "07", "8": "08", "9": "09"}
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def get_bdate() -> dict:
    file = open("PeopleInGroup.txt", 'a')
    bd = {}
    vk_session = vk_api.VkApi(token=VK_BOT_TOKEN)
    data = vk_session.method('messages.getChatUsers', dict(chat_id=36, fields="bdate", name_case="gen"))
    file.write(str(len(data)) + '\n')
    for i in data:
        if "bdate" in i:
            n = i["bdate"].split(".")
            if n[0] in nums.keys() and n[1] in nums.keys():
                bd[i["first_name"] + " " + i["last_name"]] = f"{nums[n[0]]}.{nums[n[1]]}"
            else:
                if n[0] in nums.keys():
                    bd[i["first_name"] + " " + i["last_name"]] = f"{nums[n[0]]}.{n[1]}"
                elif n[1] in nums.keys():
                    bd[i["first_name"] + " " + i["last_name"]] = f"{n[0]}.{nums[n[1]]}"
                else:
                    bd[i["first_name"] + " " + i["last_name"]] = f"{n[0]}.{n[1]}"
    return bd


def update_bdate_data():
    bd = get_bdate()
    conn = sqlite3.connect('bdate.sql')
    cursor = conn.cursor()
    file = open("PeopleInGroup.txt")
    st = file.readlines()
    if len(st) == 1:
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS bdates (id int auto_increment primary key, name varchar(50), bdate varchar(50))')
        for k, v in bd.items():
            cursor.execute("INSERT INTO bdates (name, bdate) VALUES ('%s', '%s')" % (k, v))
    elif len(st) > 1 and int(st[-1]) > int(st[-2]):
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS bdates (id int auto_increment primary key, name varchar(50), bdate varchar(50))')
        for k, v in bd.items():
            for n in cursor.fetchall():
                if k not in n:
                    cursor.execute("INSERT INTO bdates (name, bdate) VALUES ('%s', '%s')" % (k, v))

    conn.commit()
    cursor.close()
    conn.close()


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def birthday_bot_event():
    i = 0
    log.info("Hello!")
    now_date = datetime.now().strftime("%d.%m")
    date_update = True
    update_bdate_data()
    conn = sqlite3.connect("bdate.sql")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bdates")
    bd = cursor.fetchall()
    while True:
        if date_update:
            for person in bd:
                if person[2] != "":
                    if datetime.now().strftime("%d.%m") == person[2]:
                        bot.send_message(CHAT_ID, f"Сегодня день рождения у {person[1]}!")
                        i += 1
            log.info(i)
        if datetime.now().strftime("%d.%m") == now_date:
            date_update = False
        else:
            date_update = True


event_thread = Thread(target=birthday_bot_event, daemon=True)
bot_thread = Thread(target=bot.infinity_polling)
bot_thread.start()
event_thread.start()
