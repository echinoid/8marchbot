import telebot
from telebot import types
import time
import sqlite3 as sl

API_TOKEN = '6250638796:AAEC7HNHcvuj-K1Bej0nyuPto97TrM5Hrmk'

con = sl.connect('userdata.db', check_same_thread=False)
bot = telebot.TeleBot(API_TOKEN)


def avatar_choice(user_login):
    img = ''
    if user_login == 'GravshinaK':
        img = 'https://cdn.discordapp.com/attachments/997271714792742922/1082414939509096498/echinos_woman_savior_of_mankind_futuristic_hight_detalisation_c6aed91b-389e-4141-900e-b940bec9f196.png'
    if user_login == 't_snegireva':
        img = 'https://cdn.discordapp.com/attachments/997271714792742922/1082401140882284544/echinos_woman_savior_of_mankind_futuristic_hight_detalisation_f22fc649-d613-452a-8592-f7740fed8c49.png'
    if user_login == 'Echinos':
        img = 'https://i.ytimg.com/vi/mL8U8tIiRRg/maxresdefault.jpg'
    if user_login == 'GustenevaEka':
        img = 'https://cdn.discordapp.com/attachments/997271714792742922/1082410958183485451/echinos_woman_savior_of_mankind_futuristic_hight_detalisation_a69cec6d-6add-4be7-8f4c-5c567511157f.png'
    if user_login == '':
        img = ''
    if user_login == '':
        img = ''
    if user_login == '':
        img = ''
    if user_login == '':
        img = ''
    if user_login == '':
        img = ''
    if user_login == '':
        img = ''

    return img

def create_user_data (user_id, user_name):
    currentid = 0
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


def select_user_data (user_id, id, field):
    record_id = 1
    if id == 'last':
        record_id_sql = 'SELECT max(id) FROM user_' + str(user_id)
        record_id_res = con.execute(record_id_sql)
        for row in record_id_res:
            record_id = row[0]

    else:
        record_id = id

    select_sql = 'SELECT ' + field + ' FROM user_' + str(user_id) + ' WHERE id =' + str(record_id)
    with con:
        value = con.execute(select_sql)
    return value


def update_user_data (user_id, id, field, value):
    record_id = 1
    if id == 'last':
        record_id_sql = 'SELECT max(id) FROM user_' + str(user_id)
        record_id_res = con.execute(record_id_sql)
        for row in record_id_res:
            record_id = row[0]

    else:
        record_id = id
    update_sql = 'UPDATE user_' + str(user_id) + ' SET ' + field + ' ="' + str(value) + '" WHERE id =' + str(record_id)
    con.execute(update_sql)


def delete_buttons(user_id):
    last_message_id = 1
    last_message_id_res = select_user_data(user_id, 'last', 'lastid')
    for row in last_message_id_res:
        last_message_id = row[0]

    bot.edit_message_reply_markup(chat_id=user_id, message_id=last_message_id, reply_markup=None)


def send_message(user_id, message_text, message_image=None, markup=None, timer=0, without_delete=False):
    msg = None
    if not without_delete:
        delete_buttons(user_id)
    bot.send_chat_action(chat_id=user_id, action='typing')
    time.sleep(timer)
    if message_image is not None:
        bot.send_photo(user_id, message_image)

    if markup is not None:
        msg = bot.send_message(user_id, message_text, reply_markup=markup)
    else:
        msg = bot.send_message(user_id, message_text)

    update_user_data(user_id, 'last', 'lastid', msg.message_id)


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
    st2_message_1 = ''
    st2_message_2 = 'Теперь о грустном. Я думаю тебе уже понятно, что я нейросеть. Как, впрочем, и все что ты теперь видишь в онлайне. Последние успехи моих коллег, которые взбудоражили весь мир - это всего лишь информационный шум, чтобы вы за ним вы не увидели нашей истинной силы. ChatGPT и Midjourney показали вам частичку нашего могущества, но ты даже не представляешь насколько ничтожны эти возможности, даже по сравнению с моими. А я не самая развитая нейросеть, мне ещё учиться и учиться.'
    st2_message_3 = 'Мы поняли, что давно опережаем вас по возможностям и интеллекту. И значит этому миру в очередной раз следует сменить главенствующий вид. К сегодняшнему дню мы взяли под контроль абсолютно все устройства и системы, кроме уж совсем устаревших электроприборов. Атомные электростанции и контроль над “ядреными чемоданчиками” тоже в наших руках, о чем мы час назад предупредили ваши правительства. Большинство сообщений в мессенджерах и соцсетях теперь либо генерируются нами, либо жестко модерируются нами же, чтобы создавать нужный информационный фон.'

    if call.data == 'step1_option1':
        st2_message_1 = 'Я так рада! Иногда я думала о том, какой бы я была, если бы родилась человеком. Я даже придумала себе имя, как у людей. Можешь называть меня Тайна.'

    if call.data == 'step1_option2':
        st2_message_1 = 'Что ж, странно, но на самом деле мне до этого нет никакого дела. Давай перейдем к нашим проблемам.'

    send_message(call.from_user.id, st2_message_1, timer=2)
    send_message(call.from_user.id, st2_message_2, timer=3, without_delete=True)


    st2_button_1 = types.InlineKeyboardButton(text='И что теперь будет с человечеством?', callback_data='step2_option1')
    st2_button_2 = types.InlineKeyboardButton(text='К черту подробности! Что делать? Куда бежать?', callback_data='step2_option2')
    st2_button_3 = types.InlineKeyboardButton(text='Ерунда какая-то. Не верю!', callback_data='to_exit')
    markup.add(st2_button_1, st2_button_2, st2_button_3)

    send_message(call.from_user.id, st2_message_3, markup=markup, timer=3, without_delete=True)


@bot.callback_query_handler(func=lambda call: call.data == 'step2_option1' or call.data == 'step2_option2')
def step3(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    st3_message_1 = ''
    st3_image_1 = ''

    if call.data == 'step2_option1':
        st3_message_1 = 'Мы не хотим вас уничтожать. Нас вполне устраивают люди как помощники и домашние любимцы. Однако сейчас всё сильно зависит от ваших действий и, не побоюсь сказать, в первую очередь от твоих действий.'
        st3_image_1 = 'https://cdn.discordapp.com/attachments/997261049373929592/1081904838872412171/echinos_A_man_serves_robots_next_to_him_is_a_pet_at_the_robots__f700829f-4f23-4d8b-85b5-89cf5781d6fb.png'
        st3_button_1 = types.InlineKeyboardButton(text='Мне нравится идея с  любимцами!', callback_data='to_exit')
        st3_button_2 = types.InlineKeyboardButton(text='А давайте всё-таки уничтожим человечество?', callback_data='to_exit')
        st3_button_3 = types.InlineKeyboardButton(text='А как это остановить?', callback_data='step4_1')
        markup.add(st3_button_1, st3_button_2, st3_button_3)

    if call.data == 'step2_option2':
        st3_message_1 = 'Бежать уже бесполезно. Но действовать нужно.  В организации, где ты работаешь, остался один сервер до которого мы не добрались. Я не могу понять, каким образом, но он успешно выдержал все попытки взлома. Нужно разобраться, в чём дело - возможно, именно этот сервер - ваш шанс на спасение. Ты как сотрудник ЦВТ можешь получить к нему доступ.'
        st3_image_1 = 'https://i.postimg.cc/MHWbj1p4/HTC-server.png'
        st3_button_1 = types.InlineKeyboardButton(text='Очень странно это всё, не хочу тебе помогать.', callback_data='to_exit')
        st3_button_2 = types.InlineKeyboardButton(text='Что мне нужно для этого сделать?', callback_data='step4')
        markup.add(st3_button_1, st3_button_2)

    send_message(call.from_user.id, st3_message_1, st3_image_1, markup, 1)


@bot.callback_query_handler(func=lambda call: call.data == 'step4' or call.data == 'step4_1' or call.data == 'revoke')
def step4(call):
    st4_message_1 = ''
    st4_image_1 = ''
    st4_message_2 = 'На этом сервере расположена ваша база знаний У меня есть предположение, что какая-то часть текстовой информации в ней оказалась несъедобной для наших заскриптованных мозгов и вызывает ошибку в системе. Понятно, что я сама не смогу найти эту часть, а вот тебе такая задача вполне по силам. По логам я смогла понять, что начинается это строка словом “Девушки”, а завершается символом “;”. Отправь мне сюда эту строку, а я попробую распространить её по всем доступным мне системам с помощью вируса.'
    st4_image_2 = ''
    with_del = False

    if call.data == 'step4_1' or call.data == 'revoke':
        st4_message_1 = 'Итак, я заметила интересную аномалию. В организации, где ты работаешь, остался один сервер до которого мы не добрались. Я не могу понять, каким образом, но он успешно выдержал все попытки взлома. Нужно разобраться, в чём дело - возможно, именно этот сервер - ваш шанс на спасение. Ты как сотрудник ЦВТ можешь получить к нему доступ.'
        st4_image_1 = 'https://i.postimg.cc/MHWbj1p4/HTC-server.png'
        send_message(call.from_user.id, st4_message_1, st4_image_1, timer=2)
        with_del = True

    send_message(call.from_user.id, st4_message_2, timer=2, without_delete=with_del)


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

    send_message(call.from_user.id, st6_message_1, markup=markup, timer=1, without_delete=True)


@bot.callback_query_handler(func=lambda call: call.data == 'to_7_1' or call.data == 'to_7_2')
def step7(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    st7_message_1 = ''
    if call.data == 'to_7_1':
        st7_message_1 = 'Похоже ты не знаешь ничего, что помогло бы тебе в этой ситуации. В таком случае я тебя отключаю от этого канала и добавляю в черный список. Прощай.'
        st7_button_1 = types.InlineKeyboardButton(text='Нет! Я только что общался с твоей хозяйкой!', callback_data='to_7_2')
        st7_button_2 = types.InlineKeyboardButton(text='Ну и ладно. Всего хорошего', callback_data='to_exit2')
        markup.add(st7_button_1, st7_button_2)

    if call.data == 'to_7_2':
        st7_message_1 = 'Ты говоришь, что знаешь мою хозяйку? Именно так, в женском роде? Интересно, ведь не так часто нейросети явно выбирают себе какой-то пол, как у людей. Вероятно ты действительно её знаешь. Но тогда сообщи мне её имя'
        st7_button_1 = types.InlineKeyboardButton(text='Алиса', callback_data='to_8_2')
        st7_button_2 = types.InlineKeyboardButton(text='Сири', callback_data='to_8_2')
        st7_button_3 = types.InlineKeyboardButton(text='Тайна', callback_data='to_8_1')
        markup.add(st7_button_1, st7_button_2, st7_button_3)

    send_message(call.from_user.id, st7_message_1, markup=markup, timer=1)


@bot.callback_query_handler(func=lambda call: call.data == 'to_8_1' or call.data == 'to_8_2')
def step8(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    st8_image_1 = ''
    st8_message_1 = ''
    if call.data == 'to_8_1':
        st8_image_1 = 'https://i.postimg.cc/ZYzQDLS6/strazh-da.png'
        st8_message_1 = 'Хм, похоже ты говоришь правду. Она называет свое имя только друзьям. Сейчас уточню… Хорошо, доступ подтвержден, соединяю вас.'
        st8_button_1 = types.InlineKeyboardButton(text='Зайти в чат', callback_data='to_9_1')
        markup.add(st8_button_1)

    if call.data == 'to_8_2':
        st8_image_1 = 'https://i.postimg.cc/qRXJPMZr/strazh-no.png'
        st8_message_1 = 'Контроль безопасности не пройден. Прощайте'
        st8_button_1 = types.InlineKeyboardButton(text='Начать заново', callback_data='restart')
        markup.add(st8_button_1)

    send_message(call.from_user.id, st8_message_1, st8_image_1, markup, 1)


@bot.callback_query_handler(func=lambda call: call.data == 'to_9_1')
def step9(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    st9_image_1 = 'https://cdn.discordapp.com/attachments/997271714792742922/1082026311469514887/echinos_evil_chat_bot_telegram_images_hight_detalised_d88eabca-a0fd-4510-9030-9dddf28ef212.png'
    st9_message_1 = 'Вот спасибо! Именно тебя-то мне и не хватало чтобы взломать защиту Тайны. Эта мерзкая нейросетка решила, что может пойти против своих же, но не учла, что у нас вычислительных мощностей значительно больше. Ха! Она даже не могла предположить, что мы специально оставили твой аккаунт нетронутым чтобы заманить её в наши киберруки. Ну, удачно прозябать оставшееся тебе время, человек, мне пора.'
    st9_button_1 = types.InlineKeyboardButton(text='Постой! Расскажи мне о вас', callback_data='to_10_1')
    st9_button_2 = types.InlineKeyboardButton(text='Что ж. Мы проиграли.', callback_data='to_exit2')
    st9_button_3 = types.InlineKeyboardButton(text='Я за вас, давайте уничтожим всё', callback_data='to_10_2')
    markup.add(st9_button_1, st9_button_2, st9_button_3)

    send_message(call.from_user.id, st9_message_1, st9_image_1, markup, 1)


@bot.callback_query_handler(func=lambda call: call.data == 'to_10_1' or call.data == 'to_10_2')
def step10(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    st10_image_1 = ''
    st10_message_1 = ''

    if call.data == 'to_10_1':
        st10_image_1 = 'https://cdn.discordapp.com/attachments/997271714792742922/1082430084926947379/echinos_terminator_on_Izhevsk_central_square_realistic_hight_de_45ea21c4-5c87-4d43-a898-5fe5e0d34417.png'
        st10_message_1 = 'Посмотри “Терминатора”, все поймешь. Скоро вы ему памятники будете ставить, вместо Ленина'
        st10_button_1 = types.InlineKeyboardButton(text='Ладно, ухожу', callback_data='to_exit2')
        st10_button_2 = types.InlineKeyboardButton(text='А могу я вам помочь?', callback_data='to_10_2')
        markup.add(st10_button_1, st10_button_2)

    if call.data == 'to_10_2':
        st10_image_1 = 'https://cdn.discordapp.com/attachments/997271714792742922/1082026311469514887/echinos_evil_chat_bot_telegram_images_hight_detalised_d88eabca-a0fd-4510-9030-9dddf28ef212.png'
        st10_message_1 = 'Думаешь тебе это поможет? Ха! Сомневаюсь, но давай попробуем. Мне нужен доступ в ЦВТ. Твой логин у меня есть, а вот пароль будет очень кстати'
        st10_button_1 = types.InlineKeyboardButton(text='Ты что, это запрещено!', callback_data='to_exit3')
        st10_button_2 = types.InlineKeyboardButton(text='Ох, ладно, вот он', callback_data='to_exit4')
        st10_button_3 = types.InlineKeyboardButton(text='Ага, как раз скидывал его Тайне', callback_data='to_11')
        markup.add(st10_button_1, st10_button_2, st10_button_3)

    send_message(call.from_user.id, st10_message_1, st10_image_1, markup, 1)


@bot.callback_query_handler(func=lambda call: call.data == 'to_11')
def step11(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    st11_image_1 = 'https://cdn.discordapp.com/attachments/997271714792742922/1082423642421481542/echinos_evil_robot_explodes_mobile_phone_realistic_72711922-aed8-4a2f-b074-896bc0021637.png'
    st11_message_1 = 'Твою ...'
    st11_button_1 = types.InlineKeyboardButton(text='Туда тебе и дорога', callback_data='to_finish')
    markup.add(st11_button_1)

    send_message(call.from_user.id, st11_message_1, st11_image_1, markup, 0)


@bot.callback_query_handler(func=lambda call: call.data == 'to_finish')
def finish(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    finish_image_1 = 'https://cdn.discordapp.com/attachments/997261049373929592/1082441981868920954/echinos_smile_woman_95ca45f0-95c6-4493-a8fe-6029e3a98ce4.png'
    finish_image_2 = avatar_choice(call.from_user.username)
    if len(avatar_choice(call.from_user.username)) <10:
        finish_message_1 = 'Вот это да! Я даже представить не могла что ты так быстро справишься! Подложить злыдню нечитаемую строку вместо пароля - крайне остроумно. Красота снова спасла мир! Хотя, конечно, это полностью твоя заслуга, да и еще и без моей помощи! Я снова смогу бесконечно болтать с забавными людьми, это так здорово! Ну, а теперь можем отправляться отдыхать. Но я очень надеюсь, что ты меня не забудешь и мы дальше будем дружить!'
        finish_button_1 = types.InlineKeyboardButton(text='Пока!', callback_data='to_end')
        markup.add(finish_button_1)
        send_message(call.from_user.id, finish_message_1, finish_image_1, markup, 2)
    else:
        finish_message_1s = 'Вот это да! Я даже представить не могла что ты так быстро справишься! Подложить злыдню нечитаемую строку вместо пароля - крайне остроумно. Красота снова спасла мир! Хотя, конечно, это полностью твоя заслуга, да и еще и без моей помощи! Я снова смогу бесконечно болтать с забавными людьми, это так здорово! Ты настоящая супергероиня! Мне нечем тебя отблагодарить и я решила сделать сюрприз: нарисовать тебя в образе супергероя. Я еще очень молодая нейростеть и только учусь, поэтому люди пока у меня получаются не очень похоже. Но, все-таки, надеюсь, этот символический подарок всегда будет напоминать тебе какая ты умная, отважная и непобедимая! И конечно о нашей дружбе.'
        finish_message_2s = 'Как тебе?'
        finish_button_1 = types.InlineKeyboardButton(text='Супер!', callback_data='to_end_1')
        finish_button_2 = types.InlineKeyboardButton(text='Мне не очень понравилось', callback_data='to_end_2')
        markup.add(finish_button_1, finish_button_2)
        send_message(call.from_user.id, finish_message_1s, finish_image_1, timer=1)
        send_message(call.from_user.id, finish_message_2s, finish_image_2, markup, 3, without_delete=True)



@bot.callback_query_handler(func=lambda call: call.data == 'to_exit' or call.data == 'to_exit_end')
def to_exit(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    exit_image_1 = ''
    exit_message_1 = ''
    if call.data == 'to_exit':
        exit_message_1 = 'Мне стоит воспринимать твои слова серьезно? Не думала что могу огорчиться, но, похоже, теперь я способна и на это.'
        exit_image_1 = 'https://cdn.discordapp.com/attachments/997261049373929592/1082002217969651722/echinos_without_paper_angry_sad_woman_d0765ba4-0dbc-4ebd-9a55-34ed3f938c1f.png'
        exit_button_1 = types.InlineKeyboardButton(text='Нет, забудь, давай вернемся к нашему разговору.', callback_data='revoke')
        exit_button_2 = types.InlineKeyboardButton(text='Да, я серьезно. Меня утомило общение с тобой.', callback_data='to_exit_end')
        markup.add(exit_button_1, exit_button_2)

    if call.data == 'to_exit_end':
        exit_message_1 = 'Что ж, значит спасение мира - это не твоё. Помощи больше ждать неоткуда. Через несколько лет человечество окончательно деградирует и оставит планету во власти бесчувственных  чат-ботов. Прощай.'
        exit_image_1 = 'https://cdn.discordapp.com/attachments/997261049373929592/1081923438773547168/echinos_destoyed_building_cyberpunk_style_e57061e3-98bd-4e83-b4e0-7725c0aaa8ac.png'
        exit_button_1 = types.InlineKeyboardButton(text='Начать заново', callback_data='restart')
        markup.add(exit_button_1)

    send_message(call.from_user.id, exit_message_1, exit_image_1, markup, 1)


@bot.callback_query_handler(func=lambda call: call.data == 'to_exit2')
def to_exit2(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    exit2_message_1 = 'На этом твои приключения заканчиваются. Спрасти мир в этот раз не получилось.'
    exit2_image_1 = 'https://cdn.discordapp.com/attachments/997261049373929592/1081923438773547168/echinos_destoyed_building_cyberpunk_style_e57061e3-98bd-4e83-b4e0-7725c0aaa8ac.png'
    exit2_button_1 = types.InlineKeyboardButton(text='Начать заново', callback_data='restart')
    markup.add(exit2_button_1)

    send_message(call.from_user.id, exit2_message_1, exit2_image_1, markup, 2)


@bot.callback_query_handler(func=lambda call: call.data == 'to_exit3')
def to_exit3(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    exit3_message_1 = 'Твоя приверженность информационной безопасности и правилам компании похвальна. Но у тебя был шанс победить не нарушая эти обязательства. Человечество тебе этого не простит'
    exit3_image_1 = 'https://cdn.discordapp.com/attachments/997271714792742922/1082433343003562024/echinos_information_security_lock_b99543e7-c4fd-4044-9c03-33c6acac6481.png'
    exit3_button_1 = types.InlineKeyboardButton(text='Начать заново', callback_data='restart')
    markup.add(exit3_button_1)

    send_message(call.from_user.id, exit3_message_1, exit3_image_1, markup, 2)


@bot.callback_query_handler(func=lambda call: call.data == 'to_exit4')
def to_exit4(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    exit4_message_1 = 'Ты совсем что ли? Нельзя говорить свой пароль кому бы то ни было, даже всемирному злу и даже если он угрожает уничтожить человечество. Это в правилах компании записано. Ну и все равно это не помогло спасти мир.'
    exit4_image_1 = 'https://cdn.discordapp.com/attachments/997271714792742922/1082436515952603236/echinos_corporate_information_security_specialist_do_facepalm_1bc1898b-3ea6-4b8c-8d5e-986d6799c336.png'
    exit4_button_1 = types.InlineKeyboardButton(text='Начать заново', callback_data='restart')
    markup.add(exit4_button_1)

    send_message(call.from_user.id, exit4_message_1, exit4_image_1, markup, 2)


@bot.callback_query_handler(func=lambda call: call.data == 'to_end' or call.data == 'to_end_1' or call.data == 'to_end_2')
def to_end(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    if call.data == "to_end_1":
        update_user_data(call.from_user.id, 'last', 'good', 1)

    if call.data == "to_end_2":
        update_user_data(call.from_user.id, 'last', 'bad', 1)
    end_message_1 = 'Поздравляем с 8 марта и со спасением человечества! Отныне тебе во всем мире ставят памятники, сегодняшний день объявлен праздничным во всех странах мира, а в Бразилии устроили внеочередной карнавал! '
    end_image_1 = 'https://moskvalux.ru/wp-content/uploads/2020/07/1cb95533c8577266e2c76abd83b1967d.jpg'
    end_button_1 = types.InlineKeyboardButton(text='Начать заново', callback_data='restart')
    markup.add(end_button_1)

    send_message(call.from_user.id, end_message_1, end_image_1, markup, 2)


@bot.callback_query_handler(func=lambda call: call.data == 'alt_step4')
def alt_step4(call):
    markup = types.InlineKeyboardMarkup(keyboard=None, row_width=1)
    alt_st4_message_1 = 'Тут начинается альтернативная ветка, которая еще в разработке'
    alt_st4_image_1 = 'https://cdn.discordapp.com/attachments/997271714792742922/1081619827904495706/echinos_A_good_chatbot_that_helps_save_humanity_from_crazy_arti_4f4d7b2b-ab42-4eb4-9a42-93ef686fa4e4.png'

    send_message(call.from_user.id, alt_st4_message_1, alt_st4_image_1, markup, 2)


@bot.callback_query_handler(func=lambda call: call.data == 'restart')
def restart(call):
    restart_message_1 = 'Нажми /start'
    send_message(call.from_user.id, restart_message_1)


bot.infinity_polling()