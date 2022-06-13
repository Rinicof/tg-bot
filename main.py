# https://github.com/Rinicof/tg-bot
import telebot as tb

data = {}
TOKEN = '5419028605:AAGqsiNXXiipMlszQs97Sv-tTkf4EDxBi0E'
bot = tb.TeleBot(TOKEN)

cancel_markup = tb.types.InlineKeyboardMarkup()
cancel_btn = tb.types.InlineKeyboardButton('ᐊ Назад', callback_data='cancel')
cancel_markup.add(cancel_btn)

markup = tb.types.InlineKeyboardMarkup()
button_echo = tb.types.InlineKeyboardButton('Эхо-бот', callback_data='echo')
button_calc = tb.types.InlineKeyboardButton('Калькулятор', callback_data='calc')
button_photo = tb.types.InlineKeyboardButton('Фото', callback_data='photo')
markup.add(button_echo)
markup.add(button_calc)
markup.add(button_photo)

def filter_state(message):
    if message.chat.id in data:
        return True
    else:
        data[message.chat.id] = {'state':'menu'}

def filter_echo(message):
    return filter_state(message) and data[message.chat.id]['state'] == 'echo'

def filter_calc(message):
    return filter_state(message) and data[message.chat.id]['state'] == 'calc'

def filter_photo(message):
    return filter_state(message) and data[message.chat.id]['state'] == 'photo'


@bot.message_handler(commands=['start'])
def start_message(message):
    data[message.chat.id] = {'state':'start'}
    bot.send_message(
        message.chat.id, 
        message.from_user.first_name + ', нажми на кнопку, получишь результат', 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def commands(call):
    bot.answer_callback_query(call.id)
    if not call.message.chat.id in data:
        data[call.message.chat.id] = {'state':'menu'}
    else:
        if call.data == 'echo':
            bot.send_message(call.message.chat.id, 'Напиши что-то')
            data[call.message.chat.id]['state'] = 'echo'
        if call.data == 'calc':
            bot.send_message(call.message.chat.id, 'Напиши математический пример')
            data[call.message.chat.id]['state'] = 'calc'
        if call.data == 'cancel':
            bot.send_message(call.message.chat.id, 'Меню:', reply_markup=markup)
            data[call.message.chat.id]['state'] = 'menu'
        if call.data == 'photo':
            bot.send_photo(call.message.chat.id, photo='https://i.picsum.photos/id/887/500/500.jpg?hmac=lrUaX2W2WmpJkpTqueJoAhhoDXX3wDUgP1L3ZPxGwMY', caption='ваопалпрраолоывалоруцагрвыоавыиаррвыапуа', reply_markup=cancel_markup)
            data[call.message.chat.id]['state'] = 'photo'


@bot.message_handler(func=filter_calc)
def calculator(message):
    try:
        result = eval(message.text.replace('^', '**'))
        bot.send_message(message.chat.id, 'Ответ: ' + str(result), reply_markup=cancel_markup)
    except ZeroDivisionError:
        bot.send_message(message.chat.id, 'Нельзя делить на ноль!', reply_markup=cancel_markup)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так!', reply_markup=cancel_markup)

@bot.message_handler(func=filter_echo)
def echo_message(message):
    answer = message.text
    bot.reply_to(message, answer, reply_markup=cancel_markup)

@bot.message_handler(func=filter_photo)
def send_rand_photo(message):
    bot.send_photo(message.chat.id, photo='https://picsum.photos/150', caption='ваопалпрраолоывалоруцагрвыоавыиаррвыапуа')

bot.polling(non_stop=True) # Рабочий цикл бота