'''
Бот для telegram написанный под бесплатный функционал предложенного API. 
Функционал ограничен относительно эталона сравнения (евро), так же обрезаны возможности конверсии.
Функционал бота расширен по сравнению с техзаданием (в качестве компенсации)
'''




from config import TOKEN
from utils import *
import telebot

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Бот демонстрирует актуальный курс евро по отношению к разным валютам \n \
Чтобы начать работу введите команду боту в следующем формате: \n \
<имя валюты 1> <имя валюты 2> ... <имя валюты n> \n \
Чтобы конвертировать определённое количество валюты в евро, введите команду боту в формате: \n \
convert <имя валюты> <количество евро в виде целого числа или числа с точкой> \n \
Чтобы посмотреть список поддерживаемых валют введите /values'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def values_help(message: telebot.types.Message):
    text = 'доступные валюты: '
    for i in VALUES.keys():
        text = '\n'.join((text, i, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text'])
def show(message: telebot.types.Message):

    try:
        conv = Converter(message.text.lower())
        converted = conv.get_content()
        vals = ', '.join(list(conv.get_keys()))

        if 'convert' not in message.text.lower():
            costs = ', '.join(list(map(str, list(converted.values()))))
            if len(converted) > 1:
                text = str(f'курсы вaлют {vals} по отношению к евро составляют {costs}')
            else:
                text = str(f'курс валюты {vals} по отношению к евро составляет {costs}')
        else:
            raw = list(map(float, list(converted.values())))
            cost = raw[0] * conv.get_cofficient()
            text = str(f'{conv.get_cofficient()} евро стоит {cost} {vals}')

        bot.send_message(message.chat.id, text)
    except ConvertionException:
        bot.send_message(message.chat.id, f'невозможно обработать {message.text}, введите /help чтобы получить помощь')
    except ServerException:
        bot.send_message(message.chat.id, f'Невозможно подключиться к API')


if __name__ == '__main__':
    bot.polling()
