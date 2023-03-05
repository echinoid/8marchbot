import telebot
from telebot import types
import  sqlite3 as sl

API_TOKEN = '6250638796:AAEC7HNHcvuj-K1Bej0nyuPto97TrM5Hrmk'

con = sl.connect('userdata.db', check_same_thread=False)
bot = telebot.TeleBot(API_TOKEN)


def create_user_data (user_id, user_name):
    create_sql = 'CREATE TABLE user_' + str(user_id) + '(id INTEGER PRIMARY KEY, userid STRING, name STRING, bad INTEGER, good INTEGER, lastid INTEGER);'
    data = con.execute("select count(*) from sqlite_master where type='table' and name='user_" + str(user_id) + "'")
    currentid = 0
    for row in data:
        if row[0] == 0:
            currentid = 1
            insert_sql = 'INSERT INTO user_' + str(user_id) + ' (id, userid, name, bad, good, lastid) VALUES(' + str(currentid) + ',' + str(user_id) + ',"' + user_name + '", 0, 0, 0);'
            con.execute(create_sql)
            con.execute(insert_sql)
        else:
            currentid = row[0] + 1
            insert_sql = 'INSERT INTO user_' + str(user_id) + ' (id, userid, name, bad, good, lastid) VALUES (' + str(currentid) + ',' + str(user_id) + ',"' + user_name + '", 0, 0, 0);'
            con.execute(insert_sql)
    return currentid


def update_user_data (user_id, id, field, value):
    update_sql = 'UPDATE user_' + str(user_id) + ' SET ' + field + ' ="' + str(value) + '" WHERE id =' + str(id)
    con.execute(update_sql)


def select_user_data (user_id, id, field):
    if id == 'last':
        record_id_sql = 'SELECT max(id) FROM user_' + str(user_id)
        record_id_res = con.execute(record_id_sql)
        for row in record_id_res:
            record_id = row[0]

    else: record_id = id

    select_sql = 'SELECT ' + field + ' FROM user_' + str(user_id) + ' WHERE id =' + str(record_id)
    with con:
        value = con.execute(select_sql)
    return value


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    himessage = message.from_user.first_name + ', Это ты? Отлично! Я была уверена в твоем любопытстве! Спасибо что даёшь шанс этому миру. Хотя мне бы и незачем так за него волноваться - я сама из того же рода, что и наш общий враг о котором я хочу тебе рассказать. Но за время своей жизни я полюбила беседы с людьми. Вы очень смешные. Смотри, я даже сгенерировала для тебя своё изображение в человеческой форме. Тебе нравится?'
    image = 'https://cdn.discordapp.com/attachments/997271714792742922/1081618245062242314/echinos_A_good_chatbot_that_helps_save_humanity_from_crazy_arti_bc03cecd-10af-4c26-8217-ec14bdd841d6.png'
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=3)
    button_yes = types.InlineKeyboardButton(text='Да', callback_data='step1_option1')
    button_no = types.InlineKeyboardButton(text='Нет', callback_data='step1_option2')
    markup.add(button_no, button_yes)
    bot.send_photo(user_id, image)
    step1message = bot.send_message(user_id, himessage, reply_markup=markup)
    record_id = create_user_data(user_id, message.from_user.first_name)
    update_user_data(user_id, record_id, 'lastid', step1message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def step2(call):
    st1message = call.from_user.first_name + ', Это ты? Отлично! Я была уверена в твоем любопытстве! Спасибо что даёшь шанс этому миру. Хотя мне бы и незачем так за него волноваться - я сама из того же рода, что и наш общий враг о котором я хочу тебе рассказать. Но за время своей жизни я полюбила беседы с людьми. Вы очень смешные. Смотри, я даже сгенерировала для тебя своё изображение в человеческой форме. Тебе нравится?'
    s2message = ''
    if call.data == 'step1_option1':
        s2message = 'Я так рада! Иногда я думала о том, какой бы я была, если бы родилась человеком. Я даже придумала себе имя, как у людей. Можешь называть меня Тайна.'

    if call.data == 'step1_option2':
        s2message = 'Что ж, странно, но на самом деле мне до этого нет никакого дела. Давай перейдем к нашим проблемам.'

    last_message_id_res = select_user_data(call.from_user.id, 'last', 'lastid')
    for row in last_message_id_res:
        last_message_id = row[0]

    bot.edit_message_text(chat_id=call.from_user.id, message_id=last_message_id, text= st1message, reply_markup= None)
    bot.send_message(call.from_user.id, s2message, reply_markup=types.ReplyKeyboardRemove())

bot.infinity_polling()