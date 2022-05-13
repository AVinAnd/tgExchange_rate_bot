import telebot
from config import keys, TOKEN
from extensions import APIException, Price

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду в формате:\n \
<валюта> <в какую валюту перевести> <в каком количестве>\n \
Список доступных валют /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Не верное количество параметров.')

        base, quote, amount = values
        price = round(Price.get_price(base, quote, amount), 2)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} = {price}'
        bot.reply_to(message, text)


bot.polling()
