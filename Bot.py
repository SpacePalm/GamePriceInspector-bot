import telebot
import Parser
from telebot import types

bot = telebot.TeleBot("5590251989:AAGwUmFjO6OWVtljPN_IZppGVJ09u51LxGc")
message_DB = []

@bot.callback_query_handler(lambda c: c.data == 'mstart')
@bot.message_handler(commands = ["mstart"]) #мастер программы
def Mstart(messege: types.CallbackQuery):
    DeliteMessege(messege)
    markup = types.InlineKeyboardMarkup()
    onebtn = types.InlineKeyboardButton("Разовая проверка", callback_data="onecheck")
    dailybtn = types.InlineKeyboardButton("Периодическая проверка", callback_data="timecheck")
    markup.add(onebtn, dailybtn)
    bot.send_message(messege.from_user.id, "Хорошо, выберете режим работы", reply_markup=markup)

@bot.callback_query_handler(lambda c: c.data == 'help')
@bot.message_handler(commands = ["help"])
def Help(messege):
    bot.send_message(messege.from_user.id, "ge")



@bot.message_handler(commands = ["start"])
def Start(messege):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
    helpbtn = types.KeyboardButton("Давайте познакомимся?")
    startbtn = types.KeyboardButton("Продолжить без ознакомления")
    markup.add(helpbtn, startbtn)
    a = bot.send_message(messege.chat.id,"Приветствую", reply_markup = markup)
    message_DB.append(messege.message_id)
    message_DB.append(a.message_id)
    bot.register_next_step_handler(a, UnsrF)

def SetupGames(messege):
    games = messege.text
    f = open("Games.txt", "w")
    games = games.replace("/", "\n")
    f.write(games)
    f.close()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Продолжить работу", callback_data= "mstart"))
    a = bot.send_message(messege.chat.id, "Настройка успешно завершена", reply_markup= markup)
    message_DB.append(messege.message_id)
    message_DB.append(a.message_id)


def DeliteMessege(messege):
    print(message_DB)
    for i in message_DB:
        bot.delete_message(messege.from_user.id, i)
    message_DB.clear()


@bot.message_handler(content_types=['text'])
def UnsrF(messege):

    if(messege.text == "Давайте познакомимся?"):
        a = bot.send_message(messege.chat.id, "Нажмите /help, чтобы увидеть документацию", reply_markup = types.ReplyKeyboardRemove())
        message_DB.append(messege.message_id)
        message_DB.append(a.message_id)
    elif (messege.text == "Продолжить без ознакомления"):
        a = bot.send_message(messege.chat.id,"Проведем начальную настройку")
        msg = bot.send_message(messege.chat.id, 'Цены на какие игры вас интересуют? (Ввод в одном сообщении через " / ")', reply_markup = types.ReplyKeyboardRemove())
        message_DB.append(messege.message_id)
        message_DB.append(a.message_id)
        message_DB.append(msg.message_id)
        bot.register_next_step_handler(msg, SetupGames)
    else:
        a = bot.send_message(messege.chat.id, "Я вас не понимаю. Нажмите /help, чтобы увидеть документацию")
        message_DB.append(messege.message_id)
        message_DB.append(a.message_id)


bot.polling(none_stop= True)