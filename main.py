# https://github.com/Rinicof/tg-bot
import telebot
from telebot import types
from random import randint
from telebot.types import InlineKeyboardMarkup
from time import sleep
from config import *
from messages import *


bot = telebot.TeleBot(BOT_TOKEN)

cancel_markup = telebot.types.InlineKeyboardMarkup()
cancel_btn = telebot.types.InlineKeyboardButton(cancel_btn_txt, callback_data='cancel')
cancel_markup.add(cancel_btn)

markup = telebot.types.InlineKeyboardMarkup()
echo_btn = telebot.types.InlineKeyboardButton(echo_btn_txt, callback_data='echo')
calc_btn = telebot.types.InlineKeyboardButton(calc_btn_txt, callback_data='calc')
photo_btn = telebot.types.InlineKeyboardButton(photo_btn_txt, callback_data='photo')
ygadai_chislo_btn = telebot.types.InlineKeyboardButton(ygadai_chislo_btn_txt, callback_data='guess')
hack_btn = telebot.types.InlineKeyboardButton('Взломать пентагон', callback_data='hack')
markup.add(echo_btn)
markup.add(calc_btn)
markup.add(photo_btn)
markup.add(ygadai_chislo_btn)
markup.add(hack_btn)

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

confirm_markup = telebot.types.InlineKeyboardMarkup()
confirm_btn = telebot.types.InlineKeyboardButton('Подтвердить', callback_data='confirm_hack')
confirm_markup.add(confirm_btn)
confirm_markup.add(cancel_btn)


def filter_state(message):
    if message.chat.id in data:
        return True
    else:
        data[message.chat.id] = {'state': 'menu'}


def filter_main(call):
    return call.data in ['echo', 'calc', 'guess', 'cancel', 'photo', 'menu', 'hack'] 


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


def filter_hack(call):
    return call.data == 'confirm_hack'


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
        if call.data == 'hack':
            bot.send_message(call.message.chat.id, 'Точно?', reply_markup=confirm_markup)
            data[call.message.chat.id]['state'] = 'hack'
        

@bot.message_handler(func=filter_calc)
def calculator(message):
    try:
        result = eval(message.text.replace('^', '**'))
        bot.send_message(message.chat.id, 'Ответ: ' + str(result), reply_markup=cancel_markup)
    except ArithmeticError:
        bot.send_message(message.chat.id, calc_math_err_txt, reply_markup=cancel_markup)
    except:
        bot.send_message(message.chat.id, unknow_err_txt, reply_markup=cancel_markup)


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
        bot.send_message(call.message.chat.id, easy_mode_select_txt)
    elif call.data == 'medium':
        random_number = randint(0, 50)
        bot.send_message(call.message.chat.id, medium_mode_select_txt)
    elif call.data == 'hard':
        random_number = randint(0, 100)
        bot.send_message(call.message.chat.id, hard_mode_select_txt)
    data[call.message.chat.id]['state'] = 'guess'
    bot.send_message(call.message.chat.id, text=cancel_txt, reply_markup=cancel_markup)


@bot.message_handler(func=filter_guess)
def guess(message):
    try:
        if int(message.text) > random_number:
            bot.send_message(message.chat.id, guess_num_less_txt)
        elif int(message.text) < random_number:
            bot.send_message(message.chat.id, guess_num_more_txt)
        else:
            bot.send_message(message.chat.id, guess_num_equally_txt)
    except ValueError:
        bot.send_message(message.chat.id, value_err_txt)
    except:
        bot.send_message(message.chat.id, unknow_err_txt)
    bot.send_message(message.chat.id, text=cancel_txt, reply_markup=cancel_markup)


@bot.callback_query_handler(func=filter_hack)
def hack(call):
    bot.answer_callback_query(call.id)
    for i in range(0, 100):
        try:
            bot.edit_message_text(f'Взлом пентагона... {i + randint(0, 1)}%', 
            call.message.chat.id, call.message.message_id)
        except:
            pass
        sleep(0.1)
    if randint(0, 2) == 0:
        sleep(1)
        try:
            bot.edit_message_text('Упс... Похоже, ваш телефон был взломан.', 
                call.message.caht.id, call.message.message_id)
        except:
            pass
    else:
        try:
            bot.edit_message_text('Пентагон успешно взломан!', 
                call.message.chat.id, call.message.message_id)
        except:
            pass
        for i in range(0, 100):
            try:
                bot.edit_message_text(f'Поиск секретных данных об НЛО... {i + randint(0, 1)}%', 
                    call.message.chat.id, call.message.message_id)
            except:
                pass
        sleep(0.1)


bot.polling(non_stop=True)  # Рабочий цикл бота
