# https://github.com/Rinicof/tg-bot
import telebot
from telebot import types
from random import randint
from telebot.types import InlineKeyboardMarkup
from config import *
from messages import *


bot = telebot.TeleBot(BOT_TOKEN)

cancel_markup = telebot.types.InlineKeyboardMarkup()
cancel_btn = telebot.types.InlineKeyboardButton(cancel_btn_txt, callback_data='cancel')
cancel_markup.add(cancel_btn)

markup: InlineKeyboardMarkup = telebot.types.InlineKeyboardMarkup()
echo_btn = telebot.types.InlineKeyboardButton(echo_btn_txt, callback_data='echo')
calc_btn = telebot.types.InlineKeyboardButton(calc_btn_txt, callback_data='calc')
photo_btn = telebot.types.InlineKeyboardButton(photo_btn_txt, callback_data='photo')
ygadai_chislo_btn = telebot.types.InlineKeyboardButton(ygadai_chislo_btn_txt, callback_data='guess')
markup.add(echo_btn)
markup.add(calc_btn)
markup.add(photo_btn)
markup.add(ygadai_chislo_btn)

more_photo_markup = telebot.types.InlineKeyboardMarkup()
more_photo_btn = telebot.types.InlineKeyboardButton(more_btn_txt, callback_data='photo')
more_photo_markup.add(more_photo_btn)
more_photo_markup.add(cancel_btn)

selecter_mode_markup = telebot.types.InlineKeyboardMarkup()
easy_mode_btn = telebot.types.InlineKeyboardButton(easy_mode_btn_txt, callback_data='light')
medium_mode_btn = telebot.types.InlineKeyboardButton(medium_mode_btn_txt, callback_data='medium')
hard_mode_btn = telebot.types.InlineKeyboardButton(hard_mode_btn_txt, callback_data='hard')
selecter_mode_markup.add(easy_mode_btn)
selecter_mode_markup.add(medium_mode_btn)
selecter_mode_markup.add(hard_mode_btn)

def filter_state(message):
    if message.chat.id in data:
        return True
    else:
        data[message.chat.id] = {'state': 'menu'}


def filter_main(call):
    return call.data in ['echo', 'calc', 'guess', 'cancel', 'photo', 'menu'] 


def filter_echo(message):
    return filter_state(message) and data[message.chat.id]['state'] == 'echo'


def filter_calc(message):
    return filter_state(message) and data[message.chat.id]['state'] == 'calc'


def filter_photo(message):
    return filter_state(message) and data[message.chat.id]['state'] == 'photo'


def filter_diff(call):
    return call.data == 'light' or call.data == 'medium' or call.data == 'hard'


def filter_guess(message):
    return filter_state(message) and data[message.chat.id]['state'] == 'guess'


@bot.message_handler(commands=['start'])
def start_message(message):
    data[message.chat.id] = {'state': 'start'}
    bot.send_message(
        message.chat.id,
        message.from_user.first_name + first_appeal_txt,
        reply_markup=markup
    )


@bot.callback_query_handler(func=filter_main)
def commands(call):
    bot.answer_callback_query(call.id)
    if not call.message.chat.id in data:
        data[call.message.chat.id] = {'state': 'menu'}
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
            bot.send_photo(call.message.chat.id, photo=photos[randint(0, len(photos) - 1)],
                            reply_markup=more_photo_markup)
            data[call.message.chat.id]['state'] = 'photo'
        if call.data == 'guess':
            bot.send_message(call.message.chat.id, guess_message_txt, reply_markup=selecter_mode_markup)


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


@bot.callback_query_handler(func=filter_diff)
def guess_diff(call):
    bot.answer_callback_query(call.id)
    global random_number
    if call.data == 'light':
        random_number = randint(0, 10)
        bot.send_message(call.message.chat.id, 'Угадай число от 1 до 10')
    elif call.data == 'medium':
        random_number = randint(0, 50)
        bot.send_message(call.message.chat.id, 'Угадай число от 1 до 50')
    elif call.data == 'hard':
        random_number = randint(0, 100)
        bot.send_message(call.message.chat.id, 'Угадай чисо от 1 до 100')
    data[call.message.chat.id]['state'] = 'guess'
    bot.send_message(call.message.chat.id, text='Если хочешь вернуться в меню, нажми кнопку', reply_markup=cancel_markup)


@bot.message_handler(func=filter_guess)
def guess(message):
    try:
        if int(message.text) > random_number:
            bot.send_message(message.chat.id, 'Загаданное число меньше')
        elif int(message.text) < random_number:
            bot.send_message(message.chat.id, 'Загаданное число больше')
        else:
            bot.send_message(message.chat.id, 'Вы угадали')
    except:
        bot.send_message(message.chat.id, 'Ошибка. Попробуй ещё раз')
    bot.send_message(message.chat.id, text='Если хочешь вернуться в меню, нажми кнопку', reply_markup=cancel_markup)


bot.polling(non_stop=True)  # Рабочий цикл бота

