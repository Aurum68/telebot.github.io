import vk_api
import telebot
from datetime import datetime
import sqlite3

nums = {"1": "01", "2": "02", "3": "03", "4": "04", "5": "05", "6": "06", "7": "07", "8": "08", "9": "09"}


def bdate() -> dict:
    bd = {}
    vk_session = vk_api.VkApi(token="vk1.a.KroTG7TGWSgwQvFQezXp8no4ADi0vaWVgo5yBmwfLO24FKe6v2PIEMsbBeya"
                                    "-i1bBbQlL8GhlcjFL62l8hGJrUDOeAu1MyXIvSEyAbh5zfn"
                                    "-57XNQmagg70MKuL9pF_pdt6HGnRK1KVWUW7o9s8qkmkwhGnroKWPLpfaVECEHCAujircy5_"
                                    "-MUToTUQ3P446kX5b2VHfbaOAtRrJWXZQtg")
    data = vk_session.method('messages.getChatUsers', dict(chat_id=36, fields="bdate", name_case="gen"))
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


def bdate_data():
    conn = sqlite3.connect('bdate.sql')
    cursor = conn.cursor()

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS bdates (id int auto_increment primary key, name varchar(50), bdate varchar(50))')

    bd = bdate()
    for k, v in bd.items():
        cursor.execute("INSERT INTO bdates (name, bdate) VALUES ('%s', '%s')" % (k, v))

    conn.commit()
    cursor.close()
    conn.close()


bot = telebot.TeleBot("6999131337:AAE5-xPaBdkK8wtJYG5-7WsnXlJl4YEPeuw")


@bot.message_handler(commands=['start'])
def birthday_bot(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Hello!")
    now_date = datetime.now().strftime("%d.%m")
    date_update = True
    bdate_data()
    conn = sqlite3.connect('bdate.sql')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM bdates')
    bd = cursor.fetchall()
    while True:
        if date_update:
            for person in bd:
                if person[2] != "":
                    if datetime.now().strftime("%d.%m") == person[2]:
                        bot.send_message(message.chat.id, f"Сегодня день рождения у {person[1]}!")
            if datetime.now().strftime("%d.%m") == now_date:
                date_update = False
            else:
                date_update = True


bot.polling(none_stop=True)
