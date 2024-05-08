import random
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

sticker_list = ["CAACAgUAAxkBAAEMDPtmNjTlT9gRjO5j1_hMDkPpE3UqZAACPhsAAvqeaD8PN6Fuagh-_DQE",
                "CAACAgUAAxkBAAEMDP1mNjTo_o2mR_7ctxbL2SKr8yoOUwACPxsAAvqeaD9f1BdyJKBlXzQE",
                "CAACAgUAAxkBAAEMDP5mNjToRm-5zVuVBc_0Uwkr63NXmAACQBsAAvqeaD84HJobXCgQzzQE",
                "CAACAgUAAxkBAAEMDQFmNjTumzuQpQpcSAIrgrUpQruA2gACQRsAAvqeaD8Mju0iCj8iSjQE",
                "CAACAgUAAxkBAAEMDQJmNjTvqNHspfqi8Rfw3K6kNFeS_wACQhsAAvqeaD8I6YaX2mhf6zQE",
                "CAACAgUAAxkBAAEMDQNmNjTwHUGOUkeSsMZDK1goRCSmWQACQxsAAvqeaD9s98xIyIJnmDQE",
                "CAACAgUAAxkBAAEMDQRmNjTxO1YSu_S1WEcS1S-H_umgHAACRBsAAvqeaD8M1gM-ZS5j8TQE",
                "CAACAgUAAxkBAAEMDQZmNjTyWLrnX23QtzQQj3xSdioXYwACRRsAAvqeaD8r0mXtx-FzFDQE",
                "CAACAgUAAxkBAAEMDQdmNjTyDYAeCvtfNuq4rtMsoN6RoQACRhsAAvqeaD-skOaQzgzmVjQE",
                "CAACAgUAAxkBAAEMDQlmNjT0s7Khd_aP_S549zg8uSoqoQACRxsAAvqeaD_T_tRZPqzphzQE",
                "CAACAgUAAxkBAAEMDQtmNjT2qPqIcWi2HBMwkiapH_LKjQACSBsAAvqeaD9hIQjWSU2zTDQE",
                "CAACAgUAAxkBAAEMDQxmNjT2fK5KbjFm0zD_vB9jJL9RLwACSRsAAvqeaD_mWAAB0jgX1xo0BA",
                "CAACAgUAAxkBAAEMDQ1mNjT4D0e5i96qedFNAvnhQu5AUwACSxsAAvqeaD8mNMGSrUP2iDQE",
                "CAACAgUAAxkBAAEMDQ5mNjT4Si_wHf36gG-BVN1L97c6TgACShsAAvqeaD974LtFcLKoGjQE",
                "CAACAgUAAxkBAAEMDRBmNjT5442EnZUkxj5n37XhWpm9-wACTBsAAvqeaD8j0Nw6CSUpazQE",
                "CAACAgUAAxkBAAEMDRFmNjT79hO1nHONBN7kTsNiag_ZngACTRsAAvqeaD9JVrCBEUOvHzQE",
                "CAACAgUAAxkBAAEMDRJmNjT7f0OvdoTObWRK4J-zCWg13AACThsAAvqeaD_zEQI3_e8bkTQE",
                "CAACAgUAAxkBAAEMDRNmNjT8Zu9D-3iFTDnfGlxYI4zhawACTxsAAvqeaD_QQnWqckYf6TQE",
                "CAACAgUAAxkBAAEMDRVmNjT-XNCNTY_MHRVf0VNBWrbjrwACURsAAvqeaD-X2dYZJTvozzQE",
                "CAACAgUAAxkBAAEMDRZmNjT-UR0HwXBJsg4golU7FduiFQACUBsAAvqeaD97XBX-zApT4zQE",
                "CAACAgUAAxkBAAEMDRdmNjT_NOTBsjAqBq-iLbkPHjtHQgACUhsAAvqeaD99vVqD26y5xDQE",
                "CAACAgUAAxkBAAEMDRlmNjT_pMxEBEmejvog9b5ORbQvkQACUxsAAvqeaD_BK2ggEtqGOzQE",
                "CAACAgUAAxkBAAEMDRpmNjUAAeJM8EENm4O6yBMYNF80NaEAAlQbAAL6nmg_0oPdMgEcMPw0BA",
                "CAACAgUAAxkBAAEMDRtmNjUBbKot_Ufy0ymnMVO2PA4NrgACVRsAAvqeaD87WBPVmwQpWDQE",
                "CAACAgIAAxkBAAEMDO1mNjNIRgNhn3UqInr1SWowXaROHAACiwIAAladvQr3tGImDY878zQE",
                "CAACAgIAAxkBAAEMDPNmNjQmMDaZ-9YmZzJJVwWPmVvMPQACNgADMhhBJgijPPkh5sryNAQ"
                ]


def get_bdate() -> dict:
    #file = open("PeopleInGroup.txt", 'a')
    bd = {}
    vk_session = vk_api.VkApi(token=VK_BOT_TOKEN)
    data = vk_session.method('messages.getChatUsers', dict(chat_id=36, fields="bdate", name_case="gen"))
    #file.write(str(len(data)) + '\n')
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
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS bdates (id int auto_increment primary key, name varchar(50), bdate varchar(50))')
    people = cursor.execute("SELECT * FROM bdates").fetchall()
    if len(people) == 0:
        for k, v in bd.items():
            cursor.execute("INSERT INTO bdates (name, bdate) VALUES ('%s', '%s')" % (k, v))
    else:
        for k, v in bd.items():
            for person in people:
                if k not in person:
                    cursor.execute("INSERT INTO bdates (name, bdate) VALUES ('%s', '%s')" % (k, v))


    # elif len(st) > 1 and int(st[-1]) > int(st[-2]):
    #     cursor.execute(
    #         'CREATE TABLE IF NOT EXISTS bdates (id int auto_increment primary key, name varchar(50), bdate varchar(50))')
    #     for k, v in bd.items():
    #         for n in cursor.fetchall():
    #             if k not in n:
    #                 cursor.execute("INSERT INTO bdates (name, bdate) VALUES ('%s', '%s')" % (k, v))

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
                        bot.send_sticker(CHAT_ID, sticker_list[random.randint(0, len(sticker_list) - 1)])
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
