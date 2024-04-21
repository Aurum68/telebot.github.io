import vk_api
import telebot
from datetime import datetime

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
                bd[i["first_name"] + i["last_name"]] = f"{nums[n[0]]}.{nums[n[1]]}"
            else:
                if n[0] in nums.keys():
                    bd[i["first_name"] + i["last_name"]] = f"{nums[n[0]]}.{n[1]}"
                elif n[1] in nums.keys():
                    bd[i["first_name"] + i["last_name"]] = f"{n[0]}.{nums[n[1]]}"
                else:
                    bd[i["first_name"] + i["last_name"]] = f"{n[0]}.{n[1]}"
    return bd


bot = telebot.TeleBot("6999131337:AAE5-xPaBdkK8wtJYG5-7WsnXlJl4YEPeuw")


@bot.message_handler(commands=['start'])
def birthday_bot(message: telebot.types.Message):
    now_date = datetime.now().strftime("%d.%m")
    date_update = True
    bd = bdate()
    while True:
        if date_update:
            for name in bd:
                if bd[name] != "":
                    if datetime.now().strftime("%d.%m") == bd[name]:
                        bot.send_message(message.chat.id, f"Сегодня день рождения у {name}!")
            if datetime.now().strftime("%d.%m") == now_date:
                date_update = False
            else:
                date_update = True


bot.polling(none_stop=True)
