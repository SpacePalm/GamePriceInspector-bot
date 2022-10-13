import telebot
import Parser
import LoggerFile
import json
import asyncio
from telebot import types

bot = telebot.TeleBot("5590251989:AAGwUmFjO6OWVtljPN_IZppGVJ09u51LxGc")
message_DB = []
GamesCount = 0
Gamesf = True
timestart = False
timeneed = 0

@bot.callback_query_handler(lambda c: c.data == 'mstart')
@bot.message_handler(commands = ["mstart"])
def Mstart(messege: types.CallbackQuery):
    DeliteMessege(messege)
    markup = types.InlineKeyboardMarkup()
    onebtn = types.InlineKeyboardButton("Разовая проверка", callback_data="onecheck")
    dailybtn = types.InlineKeyboardButton("Периодическая проверка", callback_data="timecheck")
    markup.add(onebtn, dailybtn)
    a = bot.send_message(messege.from_user.id, "Хорошо, выберете режим работы", reply_markup=markup)
    message_DB.append(a.message_id)

@bot.callback_query_handler(lambda c: c.data == 'onecheck')
def OneCheck(messege: types.CallbackQuery):
    DeliteMessege(messege)

    a = bot.send_message(messege.from_user.id, "Ожидайте, идет поиск лучших цен на все игры с схожими названиями по запросу. Это может занять до нескольких минут...")
    message_DB.append(a.message_id)
    Parser.ParserF()
    with open("GameInfo.json", "r") as file:
        games = json.load(file)
    DeliteMessege(messege)

    markup = types.InlineKeyboardMarkup()
    onebtn = types.InlineKeyboardButton("Разовая проверка", callback_data="onecheck")
    dailybtn = types.InlineKeyboardButton("Периодическая проверка", callback_data="timecheck")
    changebtn = types.InlineKeyboardButton("Изменить список", callback_data="reset")
    markup.add(onebtn, dailybtn, changebtn)


    for i in range (0, len(games)):
        a = bot.send_message(messege.from_user.id, f"Список цен на игру {games[i]['title']}: ")
        message_DB.append(a.message_id)
        l = games[i]["Pricelist"]
        markup1 = types.InlineKeyboardMarkup()
        msg = ""
        for j in l:
            if j['price'] != "нет в наличии":
                msg += f"{j['shop_title']}: {j['price']}\n"
                s = j['shop_title']
                btn = types.InlineKeyboardButton(s, url=j['link'])
                markup1.add(btn)
            else:
                pass
        if msg == "":
            a = bot.send_message(messege.from_user.id,"К сожалению данной игры нет в наличии ни в одном из доступных магазинов")
            message_DB.append(a.message_id)
        else:
            a = bot.send_message(messege.from_user.id,msg,  reply_markup=markup1)
            message_DB.append(a.message_id)


    if len(games) < GamesCount:
        bot.send_message(messege.from_user.id, "Одно или несколько названий были введены некорректно, повторите ввод")

    a = bot.send_message(messege.from_user.id, "Выберете режим работы", reply_markup=markup)
    message_DB.append(a.message_id)


# @bot.callback_query_handler(lambda c: c.data == 'timecheck')
# def TimeCheck(messege: types.CallbackQuery):
#     timestart = True
#     DeliteMessege(messege)
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     onedaybtn = types.InlineKeyboardButton("Каждый день", callback_data="oneday")
#     weekbtn = types.InlineKeyboardButton("Каждую неделю", callback_data="week")
#     threedaysbtn = types.InlineKeyboardButton("каждые три дня", callback_data="threedays")
#     markup.add(onedaybtn, weekbtn, threedaysbtn)
#     a = bot.send_message(messege.from_user.id, "С какой периодичностью вам напоминать?", reply_markup=markup)
#     message_DB.append(a.message_id)
#     currenttime = date.today()
#     @bot.callback_query_handler(func=lambda c: True)
#     def DaysChecking(c):
#         if c.data == "oneday": # One day fnc
#             timeneed = currenttime + timedelta(days=1)
#         if c.data == "week": # Week fnc
#             timeneed = currenttime + timedelta(days=7)
#         if c.data == "threedays": # Three days fnc
#             timeneed = currenttime + timedelta(days=3)
#


@bot.callback_query_handler(lambda c: c.data == 'help')
@bot.message_handler(commands = ["help"])
def Help(messege):
    message_DB.append(messege.message_id)
    a = bot.send_message(messege.from_user.id, "Данный бот работает как поисковик цен на игры, вы вводите названия, а бот ищет доступные цены. Если вы не обнаружили ваш любмый магазин, не беспокойтесь, он будет добавле в ближайшее время. Для корректной работы бота нажмите /start или выберете в списке команд и следуйте инструкции.")
    message_DB.append(a.message_id)


@bot.message_handler(commands = ["start"])
def Start(messege):
    markup = types.InlineKeyboardMarkup(row_width = 1)
    helpbtn = types.InlineKeyboardButton("Давайте познакомимся?", callback_data= "welcome")
    startbtn = types.InlineKeyboardButton("Продолжить без ознакомления", callback_data = "reset")
    markup.add(helpbtn, startbtn)
    a = bot.send_message(messege.chat.id,"Приветствую", reply_markup = markup)

    message_DB.append(a.message_id)


def SetupGames(messege):
    global GamesCount, Gamesf
    Gamesf = True
    games = messege.text
    with open("JsonList.json", "w") as file:
        GamesCount = games.count("/") + 1
        games = games.split("/")
        json.dump(games, file, indent=5)
    file.close()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Продолжить работу", callback_data= "mstart"), types.InlineKeyboardButton("Перезаписать названия", callback_data= "reset"))
    a = bot.send_message(messege.chat.id, "Настройка успешно завершена", reply_markup= markup)
    message_DB.append(messege.message_id)
    message_DB.append(a.message_id)


def DeliteMessege(messege):
    LoggerFile.logger.info(message_DB)
    for i in message_DB:
        bot.delete_message(messege.from_user.id, i)
    message_DB.clear()

@bot.callback_query_handler(lambda c: c.data == 'reset')
def Reset(messege: types.CallbackQuery):
    global  Gamesf
    DeliteMessege(messege)
    msg = bot.send_message(messege.from_user.id, 'Проведем настройку\nЦены на какие игры вас интересуют? (Ввод в одном сообщении через " / ")', reply_markup=types.ReplyKeyboardRemove())
    message_DB.append(msg.message_id)
    Gamesf = False
    bot.register_next_step_handler(msg, SetupGames)

@bot.callback_query_handler(lambda c: c.data == 'welcome')
def Welcome(messege: types.CallbackQuery):
    DeliteMessege(messege)
    a = bot.send_message(messege.from_user.id, "Нажмите /help, чтобы увидеть документацию", reply_markup=types.ReplyKeyboardRemove())
    # message_DB.append(messege.message_id)
    message_DB.append(a.message_id)



@bot.message_handler(content_types=['text'])
def UnsrF(messege):
    if Gamesf:
        a = bot.send_message(messege.chat.id, "Я вас не понимаю. Нажмите /help, чтобы увидеть документацию")
        message_DB.append(messege.message_id)
        message_DB.append(a.message_id)

#asyncio.run(Parser.Timer())
bot.polling(none_stop= True)
