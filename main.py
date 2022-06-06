# https://github.com/Rinicof/tg-bot
import telebot as tb

data = {}
TOKEN = '5419028605:AAGqsiNXXiipMlszQs97Sv-tTkf4EDxBi0E'
bot = tb.TeleBot(TOKEN)

def filter_echo(message):
    return data[message.chat.id]['state'] == 'echo'

@bot.message_handler(commands=['start'])
def start_message(message):
    data[message.chat.id] = {'state':'start'}
    markup = tb.types.InlineKeyboardMarkup()
    button_echo = tb.types.InlineKeyboardButton('Эхо-бот', callback_data='echo')
    markup.add(button_echo)
    bot.send_message(
        message.chat.id, 
        message.from_user.first_name + ', нажми на кнопку, получишь результат', 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def commands(call):
    bot.answer_callback_query(call.id)
    if call.data == 'echo':
        bot.send_message(call.message.chat.id, 'Напиши что-то')
        data[call.message.chat.id]['state'] = 'echo'

@bot.message_handler(func=filter_echo)
def echo_message(message):
    answer = message.text
    bot.reply_to(message, answer)


bot.polling(non_stop=True) # Рабочий цикл бота
