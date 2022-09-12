import telebot
import Parser
import LoggerFile
import json
from telebot import types

bot = telebot.TeleBot("5590251989:AAGwUmFjO6OWVtljPN_IZppGVJ09u51LxGc")
message_DB = []
GamesCount = 0
Gamesf = True

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

    a = bot.send_message(messege.from_user.id, "Ожидайте, идет поиск лучших цен на игры по запросу. Это может занять до нескольких минут...")
    message_DB.append(a.message_id)
    games = Parser.ParserF()
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
        for j in l:# нахуй индексы используем прогон по элементам

            msg += f"{j['shop_title']}: {j['price']}\n"
#            if l[j]['price'] != "нет в наличии":
#                s = l[j]['shop_title']
#                btn = types.InlineKeyboardButton(s, url=l[j]['link'])
#                markup1.add(btn)
#            else:
#                pass
        a = bot.send_message(messege.from_user.id,msg,  reply_markup=markup1)
        message_DB.append(a.message_id)

    if len(games) != GamesCount:
        bot.send_message(messege.from_user.id, "Одно или несколько названий были введены некорректно, повторите ввод")

    a = bot.send_message(messege.from_user.id, "Выберете режим работы", reply_markup=markup)
    message_DB.append(a.message_id)

    #DeliteMessege(messege)




@bot.callback_query_handler(lambda c: c.data == 'help')
@bot.message_handler(commands = ["help"])
def Help(messege):
    bot.send_message(messege.from_user.id, "ge")



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
        json.dump(games, file)
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
    message_DB.append(messege.message_id)
    message_DB.append(a.message_id)


@bot.message_handler(content_types=['text'])
def UnsrF(messege):
    if Gamesf:
        a = bot.send_message(messege.chat.id, "Я вас не понимаю. Нажмите /help, чтобы увидеть документацию")
        message_DB.append(messege.message_id)
        message_DB.append(a.message_id)


bot.polling(none_stop= True)