# https://github.com/Rinicof/tg-bot
import telebot as tb
from random import randint
from config import *
from messages import *

bot = tb.TeleBot(BOT_TOKEN)

cancel_markup = tb.types.InlineKeyboardMarkup()
cancel_btn = tb.types.InlineKeyboardButton(cancel_btn_txt, callback_data='cancel')
cancel_markup.add(cancel_btn)

markup = tb.types.InlineKeyboardMarkup()
echo_btn = tb.types.InlineKeyboardButton(echo_btn_txt, callback_data='echo')
calc_btn = tb.types.InlineKeyboardButton(calc_btn_txt, callback_data='calc')
photo_btn = tb.types.InlineKeyboardButton(photo_btn_txt, callback_data='photo')
markup.add(echo_btn)
markup.add(calc_btn)
markup.add(photo_btn)

more_photo_markup = tb.types.InlineKeyboardMarkup()
more_photo_btn = tb.types.InlineKeyboardButton(more_btn_txt, callback_data='photo')
more_photo_markup.add(more_photo_btn)
more_photo_markup.add(cancel_btn)

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
        message.from_user.first_name + first_appeal_txt, 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def commands(call):
    bot.answer_callback_query(call.id)
    if not call.message.chat.id in data:
        data[call.message.chat.id] = {'state':'menu'}
    else:
        if call.data == 'echo':
            bot.send_message(call.message.chat.id, echo_message_txt)
            data[call.message.chat.id]['state'] = 'echo'
        if call.data == 'calc':
            bot.send_message(call.message.chat.id, calc_message_txt)
            data[call.message.chat.id]['state'] = 'calc'
        if call.data == 'cancel':
            bot.send_message(call.message.chat.id, menu_message_txt, reply_markup=markup)
            data[call.message.chat.id]['state'] = 'menu'
        if call.data == 'photo':
            bot.send_photo(call.message.chat.id, photo=photos[randint(0, len(photos) - 1)], reply_markup=more_photo_markup)
            data[call.message.chat.id]['state'] = 'photo'


@bot.message_handler(func=filter_calc)
def calculator(message):
    try:
        result = eval(message.text.replace('^', '**'))
        bot.send_message(message.chat.id, 'Ответ: ' + str(result), reply_markup=cancel_markup)
    except ZeroDivisionError:
        bot.send_message(message.chat.id, calc_division_err_txt, reply_markup=cancel_markup)
    except:
        bot.send_message(message.chat.id, calc_unknow_err_txt, reply_markup=cancel_markup)

@bot.message_handler(func=filter_echo)
def echo_message(message):
    answer = message.text
    bot.reply_to(message, answer, reply_markup=cancel_markup)


bot.polling(non_stop=True) # Рабочий цикл бота
