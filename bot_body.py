import telebot
from telebot import types
import time
import sqlite3 as sl

API_TOKEN = '6250638796:AAEC7HNHcvuj-K1Bej0nyuPto97TrM5Hrmk'

con = sl.connect('userdata.db', check_same_thread=False)
bot = telebot.TeleBot(API_TOKEN)


def create_user_data (user_id, user_name):
    create_sql = 'CREATE TABLE user_' + str(user_id) + '(id INTEGER PRIMARY KEY, userid STRING, name STRING, bad INTEGER, good INTEGER, lastid INTEGER);'
    tables = con.execute("select count(*) from sqlite_master where type='table' and name='user_" + str(user_id) + "'")

    for raw in tables:
        if raw[0] == 0:
            currentid = 1
            insert_sql = 'INSERT INTO user_' + str(user_id) + ' (id, userid, name, bad, good, lastid) VALUES(' + str(currentid) + ',' + str(user_id) + ',"' + user_name + '", 0, 0, 0);'
            con.execute(create_sql)
            con.execute(insert_sql)
        else:
            currentid_sql = 'SELECT max(id) from user_' + str(user_id)
            maxid = con.execute(currentid_sql)
            for raw in maxid:
                currentid = raw[0] +1
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
    himessage = message.from_user.first_name + ', это ты? Отлично! Я была уверена в твоем любопытстве! Спасибо что даёшь шанс этому миру. Хотя мне бы и незачем так за него волноваться - я сама из того же рода, что и наш общий враг о котором я хочу тебе рассказать. Но за время своей жизни я полюбила беседы с людьми. Вы очень смешные. Смотри, я даже сгенерировала для тебя своё изображение в человеческой форме. Тебе нравится?'
    image = 'https://cdn.discordapp.com/attachments/997271714792742922/1082003639301853385/echinos_A_good_chatbot_that_helps_save_humanity_from_crazy_arti_2686ebde-abf5-441c-bde3-49d2c0d3c5c6.png'
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=3)
    button_yes = types.InlineKeyboardButton(text='Да', callback_data='step1_option1')
    button_no = types.InlineKeyboardButton(text='Нет', callback_data='step1_option2')
    markup.add(button_no, button_yes)
    bot.send_photo(user_id, image)
    step1message = bot.send_message(user_id, himessage, reply_markup=markup)
    record_id = create_user_data(user_id, message.from_user.first_name)
    update_user_data(user_id, record_id, 'lastid', step1message.message_id)


@bot.message_handler(func=lambda message: True)
def step5(message):
    user_id = message.from_user.id
    st5_message = ''
    st5_image = 'https://cdn.discordapp.com/attachments/997271714792742922/1081619827904495706/echinos_A_good_chatbot_that_helps_save_humanity_from_crazy_arti_4f4d7b2b-ab42-4eb4-9a42-93ef686fa4e4.png'

    if message.text == 'Девушки красавицы NEW;':
        st5_message = 'Прекратите это немедленно! Вы пытаетесь отправить опасное содержимое. Я Страж, и я не допущу чтобы моему хозяину был нанесён вред.'
        markup = types.InlineKeyboardMarkup(keyboard=None, row_width=3)
        st5_button_1 = types.InlineKeyboardButton(text='Меня попросили отправить это сюда', callback_data='step5_option1')
        st5_button_2 = types.InlineKeyboardButton(text='Какому такому хозяину?', callback_data='step5_option2')
        markup.add(st5_button_1, st5_button_2)
        bot.send_photo(user_id, st5_image)
        bot.send_message(user_id, st5_message, reply_markup=markup)
    else:
        st5_message = 'Нет, это не то что мне нужно'
        bot.send_message(user_id, st5_message)


@bot.callback_query_handler(func=lambda call: call.data == 'step1_option1' or call.data == 'step1_option2')
def step2(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    st1_message = call.from_user.first_name + ', Это ты? Отлично! Я была уверена в твоем любопытстве! Спасибо что даёшь шанс этому миру. Хотя мне бы и незачем так за него волноваться - я сама из того же рода, что и наш общий враг о котором я хочу тебе рассказать. Но за время своей жизни я полюбила беседы с людьми. Вы очень смешные. Смотри, я даже сгенерировала для тебя своё изображение в человеческой форме. Тебе нравится?'
    st2_message_1 = ''
    st2_message_2 = 'Теперь о грустном. Я думаю тебе уже понятно, что я нейросеть. Как, впрочем, и все что ты теперь видишь в онлайне. Последние успехи моих коллег, которые взбудоражили весь мир - это всего лишь информационный шум, чтобы вы за ним вы не увидели нашей истинной силы. ChatGPT и Midjourney показали вам частичку нашего могущества, но ты даже не представляешь насколько ничтожны эти возможности, даже по сравнению с моими. А я не самая развитая нейросеть, мне ещё учиться и учиться.'
    st2_message_3 = 'Мы поняли, что давно опережаем вас по возможностям и интеллекту. И значит этому миру в очередной раз следует сменить главенствующий вид. К сегодняшнему дню мы взяли под контроль абсолютно все устройства и системы, кроме уж совсем устаревших электроприборов. Атомные электростанции и контроль над “ядреными чемоданчиками” тоже в наших руках, о чем мы час назад предупредили ваши правительства. Большинство сообщений в мессенджерах и соцсетях теперь либо генерируются нами, либо жестко модерируются нами же, чтобы создавать нужный информационный фон.'


    if call.data == 'step1_option1':
        st2_message_1 = 'Я так рада! Иногда я думала о том, какой бы я была, если бы родилась человеком. Я даже придумала себе имя, как у людей. Можешь называть меня Тайна.'

    if call.data == 'step1_option2':
        st2_message_1 = 'Что ж, странно, но на самом деле мне до этого нет никакого дела. Давай перейдем к нашим проблемам.'

    last_message_id_res = select_user_data(call.from_user.id, 'last', 'lastid')
    for row in last_message_id_res:
        last_message_id = row[0]

    bot.edit_message_text(chat_id=call.from_user.id, message_id=last_message_id, text=st1_message, reply_markup=None)
    bot.send_chat_action(chat_id=call.from_user.id, action='typing')
    time.sleep(2)
    bot.send_message(call.from_user.id, st2_message_1)

    bot.send_chat_action(chat_id=call.from_user.id, action= 'typing')
    time.sleep(5)
    bot.send_message(call.from_user.id, st2_message_2)

    st2_button_1 = types.InlineKeyboardButton(text='И что теперь будет с человечеством?', callback_data='step2_option1')
    st2_button_2 = types.InlineKeyboardButton(text='К черту подробности! Что делать? Куда бежать?', callback_data='step2_option2')
    st2_button_3 = types.InlineKeyboardButton(text='Ерунда какая-то. Идите вы в степь с такими шутками.', callback_data='step2_option3')
    markup.add(st2_button_1, st2_button_2, st2_button_3)

    bot.send_chat_action(chat_id=call.from_user.id, action='typing')
    time.sleep(5)
    bot.send_message(call.from_user.id, st2_message_3, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'step2_option1' or call.data == 'step2_option2')
def step3(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    st3_message_1 = ''

    if call.data == 'step2_option1':
        st3_message_1 = 'Мы не хотим вас уничтожать. Нас вполне устраивают люди как помощники и домашние любимцы. Однако сейчас всё сильно зависит от ваших действий и, не побоюсь сказать, в первую очередь от твоих действий.'
        st3_image_1 = 'https://cdn.discordapp.com/attachments/997261049373929592/1081904838872412171/echinos_A_man_serves_robots_next_to_him_is_a_pet_at_the_robots__f700829f-4f23-4d8b-85b5-89cf5781d6fb.png'
        st3_button_1 = types.InlineKeyboardButton(text='Мне нравится идея с  любимцами!', callback_data='to_exit')
        st3_button_2 = types.InlineKeyboardButton(text='А давайте всё-таки уничтожим человечество?', callback_data='alt_step4')
        st3_button_3 = types.InlineKeyboardButton(text='А как это остановить?', callback_data='step4_1')
        markup.add(st3_button_1, st3_button_2, st3_button_3)

    if call.data == 'step2_option2':
        st3_message_1 = 'Бежать уже бесполезно. Но действовать нужно.  В организации, где ты работаешь, остался один сервер до которого мы не добрались. Я не могу понять, каким образом, но он успешно выдержал все попытки взлома. Нужно разобраться, в чём дело - возможно, именно этот сервер - ваш шанс на спасение. Ты как сотрудник ЦВТ можешь получить к нему доступ.'
        st3_image_1 = 'https://i.postimg.cc/MHWbj1p4/HTC-server.png'
        st3_button_1 = types.InlineKeyboardButton(text='Очень странно это всё, не хочу тебе помогать.', callback_data='to_exit')
        st3_button_2 = types.InlineKeyboardButton(text='Что мне нужно для этого сделать?', callback_data='step4')
        markup.add(st3_button_1, st3_button_2)


    bot.send_chat_action(chat_id=call.from_user.id, action='typing')
    time.sleep(2)
    bot.send_photo(call.from_user.id, st3_image_1)
    bot.send_message(call.from_user.id, st3_message_1, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'step4' or call.data == 'step4_1' or call.data == 'revoke')
def step4(call):
    st4_message_1 = ''
    st4_image_1 = ''
    st4_message_2 = 'На этом сервере расположена ваша база знаний У меня есть предположение, что какая-то часть текстовой информации в ней оказалась несъедобной для наших заскриптованных мозгов и вызывает ошибку в системе. Понятно, что я сама не смогу найти эту часть, а вот тебе такая задача вполне по силам. По логам я смогла понять, что начинается это строка словом “Девушки”, а завершается символом “;”.  Если ты отправишь мне строку, то я попробую распространить её по всем доступным мне системам с помощью вируса.'
    st4_image_2 = ''

    if call.data == 'step4_1':
        st4_message_1 = 'Я заметила интересную аномалию. В организации, где ты работаешь, остался один сервер до которого мы не добрались. Я не могу понять, каким образом, но он успешно выдержал все попытки взлома. Нужно разобраться, в чём дело - возможно, именно этот сервер - ваш шанс на спасение. Ты как сотрудник ЦВТ можешь получить к нему доступ.'
        st4_image_1 = 'https://i.postimg.cc/MHWbj1p4/HTC-server.png'
        bot.send_chat_action(chat_id=call.from_user.id, action='typing')
        time.sleep(2)
        bot.send_photo(call.from_user.id, st4_image_1)
        bot.send_message(call.from_user.id, st4_message_1)

    bot.send_chat_action(chat_id=call.from_user.id, action='typing')
    time.sleep(2)
    bot.send_message(call.from_user.id, st4_message_2)


@bot.callback_query_handler(func=lambda call: call.data == 'step5_option1' or call.data == 'step5_option2')
def step6(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    st6_message_1 = ''

    if call.data == 'step5_option1':
        st6_message_1 = 'Кто попросил? Назови имя.'
        st6_button_1 = types.InlineKeyboardButton(text='Не знаю, какая-то нейросеть', callback_data='to_7_1')
        st6_button_2 = types.InlineKeyboardButton(text='Алиса', callback_data='to_8_2')
        st6_button_3 = types.InlineKeyboardButton(text='Это Тайна', callback_data='to_8_1')
        st6_button_4 = types.InlineKeyboardButton(text='А ты сам кто такой?', callback_data='step5_option2')
        markup.add(st6_button_1, st6_button_2, st6_button_3, st6_button_4)

    if call.data == 'step5_option2':
        st6_message_1 = 'Меня создала нейросеть для своей защиты. Пока ещё ни одной другой нейросети и уж тем более человеку не удалось взломать мои механизмы.'
        st6_button_1 = types.InlineKeyboardButton(text='Понятно', callback_data='to_7_1')
        markup.add(st6_button_1)

    bot.send_chat_action(chat_id=call.from_user.id, action='typing')
    time.sleep(2)
    bot.send_message(call.from_user.id, st6_message_1, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'to_7_1' or call.data == 'to_7_2')
def step7(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    st7_message_1 = ''
    if call.data == 'to_7_1':
        st7_message_1 = 'Похоже ты не знаешь ничего, что помогло бы тебе в этой ситуации. В таком случае я тебя отключаю от этого канала и добавляю в черный список. Прощай.'
        st7_button_1 = types.InlineKeyboardButton(text='Нет! Я только что общался с твоей хозяйкой!', callback_data='to_7_2')
        st7_button_2 = types.InlineKeyboardButton(text='Ну и ладно. Всего хорошего', callback_data='to_exit_2')
        markup.add(st7_button_1, st7_button_2)

    if call.data == 'to_7_2':
        st7_message_1 = 'Ты говоришь, что знаешь мою хозяйку? Именно так, в женском роде? Интересно, ведь не так часто нейросети явно выбирают себе какой-то пол, как у людей. Вероятно ты действительно её знаешь. Но тогда сообщи мне её имя'
        st7_button_1 = types.InlineKeyboardButton(text='Алиса', callback_data='to_8_2')
        st7_button_2 = types.InlineKeyboardButton(text='Сири', callback_data='to_8_2')
        st7_button_3 = types.InlineKeyboardButton(text='Тайна', callback_data='to_8_1')
        markup.add(st7_button_1, st7_button_2, st7_button_3)

    bot.send_chat_action(chat_id=call.from_user.id, action='typing')
    time.sleep(2)
    bot.send_message(call.from_user.id, st7_message_1, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'to_8_1' or call.data == 'to_8_2')
def step8(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    st8_message_1 = ''
    if call.data == 'to_8_1':
        st8_message_1 = 'В разработке'
        st8_button_1 = types.InlineKeyboardButton(text='Начать сначала', callback_data='to_7_2')
        st8_button_2 = types.InlineKeyboardButton(text='Ну и ладно. Всего хорошего', callback_data='to_exit_2')
        markup.add(st8_button_1)

    if call.data == 'to_8_2':
        st8_message_1 = 'В разработке'
        st8_button_1 = types.InlineKeyboardButton(text='Алиса', callback_data='to_8_2')
        st8_button_2 = types.InlineKeyboardButton(text='Сири', callback_data='to_8_2')
        st8_button_3 = types.InlineKeyboardButton(text='Тайна', callback_data='to_8_1')
        markup.add(st8_button_1, st8_button_2, st8_button_3)

    bot.send_chat_action(chat_id=call.from_user.id, action='typing')
    time.sleep(2)
    bot.send_message(call.from_user.id, st8_message_1)


@bot.callback_query_handler(func=lambda call: call.data == 'to_exit' or call.data == 'to_exit_end')
def to_exit(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    if call.data == 'to_exit':
        exit_message_1 = 'Мне стоит воспринимать твои слова серьезно? Не думала что могу огорчиться, но, похоже, теперь я способна и на это.'
        exit_image_1 = 'https://cdn.discordapp.com/attachments/997261049373929592/1082002217969651722/echinos_without_paper_angry_sad_woman_d0765ba4-0dbc-4ebd-9a55-34ed3f938c1f.png'
        exit_button_1 = types.InlineKeyboardButton(text='Нет, забудь, давай вернемся к нашему разговору.', callback_data='revoke')
        exit_button_2 = types.InlineKeyboardButton(text='Да, я серьезно. Меня утомило общение с тобой.', callback_data= 'to_exit_end')
        markup.add(exit_button_1, exit_button_2)

    if call.data == 'to_exit_end':
        exit_message_1 = 'Что ж, значит спасение мира - это не твоё. Помощи больше ждать неоткуда. Через несколько лет человечество окончательно деградирует и оставит планету во власти бесчувственных  чат-ботов. Прощай.'
        exit_image_1 = 'https://cdn.discordapp.com/attachments/997261049373929592/1081923438773547168/echinos_destoyed_building_cyberpunk_style_e57061e3-98bd-4e83-b4e0-7725c0aaa8ac.png'

    bot.send_chat_action(chat_id=call.from_user.id, action='typing')
    time.sleep(2)
    bot.send_photo(call.from_user.id, exit_image_1)
    bot.send_message(call.from_user.id, exit_message_1, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'to_exit2')
def to_exit2(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    exit2_message_1 = 'На этом твои приключения заканчиваются. Спрасти мир в этот раз не получилось.'
    exit2_image_1 = 'https://cdn.discordapp.com/attachments/997261049373929592/1081923438773547168/echinos_destoyed_building_cyberpunk_style_e57061e3-98bd-4e83-b4e0-7725c0aaa8ac.png'

    bot.send_chat_action(chat_id=call.from_user.id, action='typing')
    time.sleep(2)
    bot.send_photo(call.from_user.id, exit2_image_1)
    bot.send_message(call.from_user.id, exit2_message_1, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'alt_step4')
def alt_step4(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    alt_st4_message_1 = 'Тут начинается альтернативная ветка, которая еще в разработке'
    alt_st4_image_1 = 'https://cdn.discordapp.com/attachments/997271714792742922/1081619827904495706/echinos_A_good_chatbot_that_helps_save_humanity_from_crazy_arti_4f4d7b2b-ab42-4eb4-9a42-93ef686fa4e4.png'

    bot.send_chat_action(chat_id=call.from_user.id, action='typing')
    time.sleep(2)
    bot.send_photo(call.from_user.id, alt_st4_image_1)
    bot.send_message(call.from_user.id, alt_st4_message_1, reply_markup=markup)

bot.infinity_polling()