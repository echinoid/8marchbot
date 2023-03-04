import telebot

API_TOKEN = '6250638796:AAEC7HNHcvuj-K1Bej0nyuPto97TrM5Hrmk'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text:
        bot.send_message(message.from_user.id, 'aaaaaaaaa')


bot.polling(none_stop=True, interval=0)