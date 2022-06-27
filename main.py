# https://github.com/Rinicof/tg-bot
from audioop import maxpp
from calendar import c
from subprocess import call
import telebot
from telebot import types
from telebot.types import *
from random import randint
from time import sleep
import urllib
import re
import requests as req
import os
import json
from config import *
from messages import *



bot = telebot.TeleBot (BOT_TOKEN)

cancel_markup = telebot.types.InlineKeyboardMarkup ()
cancel_btn = telebot.types.InlineKeyboardButton (
    MESSAGES [
        "cancel_btn_txt"
    ], 
    callback_data="cancel"
)
cancel_markup.add (cancel_btn)

markup = telebot.types.InlineKeyboardMarkup ()
echo_btn = telebot.types.InlineKeyboardButton (
    MESSAGES [
        "echo_btn_txt"
    ], 
    callback_data="echo"
)
calc_btn = telebot.types.InlineKeyboardButton (
    MESSAGES [
        "calc_btn_txt"
    ], 
    callback_data="calc"
)
photo_btn = telebot.types.InlineKeyboardButton (
    MESSAGES [
        "photo_btn_txt"
    ], 
    callback_data="photo"
    )
ygadai_chislo_btn = telebot.types.InlineKeyboardButton (
    MESSAGES [
        "ygadai_chislo_btn_txt"
    ], 
    callback_data="guess"
)
hack_btn = telebot.types.InlineKeyboardButton (
    MESSAGES [
        "hack_btn_txt"
    ], 
    callback_data="hack"
)
shop_btn = telebot.types.InlineKeyboardButton (
    "Магазин",
    callback_data="shop"
)
search_yt_btn = telebot.types.InlineKeyboardButton (
    "Поиск видео", 
    callback_data="yt_search"
)
send_sticker_btn = telebot.types.InlineKeyboardButton (
    "Стикер",
    callback_data="send_sticker"
)
markup.add (echo_btn)
markup.add (calc_btn)
markup.add (photo_btn)
markup.add (ygadai_chislo_btn)
markup.add (hack_btn)
markup.add (shop_btn)
markup.add (search_yt_btn)
markup.add (send_sticker_btn)

more_photo_markup = telebot.types.InlineKeyboardMarkup ()
more_photo_btn = telebot.types.InlineKeyboardButton (
    MESSAGES [
        "more_btn_txt"
    ], 
    callback_data="photo"
)
more_photo_markup.add (more_photo_btn)
more_photo_markup.add (cancel_btn)

selecter_mode_markup = telebot.types.InlineKeyboardMarkup ()
easy_mode_btn = telebot.types.InlineKeyboardButton (
    MESSAGES [
        "easy_mode_btn_txt"
    ], 
    callback_data="light"
)
medium_mode_btn = telebot.types.InlineKeyboardButton (
    MESSAGES [
        "medium_mode_btn_txt"
    ], 
    callback_data="medium"
)
hard_mode_btn = telebot.types.InlineKeyboardButton (
    MESSAGES [
        "hard_mode_btn_txt"
    ], 
    callback_data="hard"
)
selecter_mode_markup.add (easy_mode_btn)
selecter_mode_markup.add (medium_mode_btn)
selecter_mode_markup.add (hard_mode_btn)

confirm_markup = telebot.types.InlineKeyboardMarkup ()
confirm_btn = telebot.types.InlineKeyboardButton (
    "Подтвердить", 
    callback_data="confirm_hack"
)
confirm_markup.add (confirm_btn)
confirm_markup.add (cancel_btn)

shop_markup = telebot.types.InlineKeyboardMarkup ()
buy_pineapple_btn = telebot.types.InlineKeyboardButton (
    "Ананас - ₽249",
    callback_data="buy_pineapple"
)
buy_dragon_fruit_btn = telebot.types.InlineKeyboardButton (
    "Драгон фрукт - ₽549",
    callback_data="buy_dragon_fruit"
)
shop_markup.add (buy_pineapple_btn)
shop_markup.add (buy_dragon_fruit_btn)

regexp = r"watch\?v=(\S{11})"
pattern = re.compile (regexp)
url = "https://www.youtube.com/results?"

file_markup = telebot.types.ReplyKeyboardMarkup (one_time_keyboard=True)
sticker_button = telebot.types.KeyboardButton ("Стикер")
file_markup.add (sticker_button)

def filter_state (message):
    if message.chat.id in data:
        return True
    else:
        data [message.chat.id] = {"state": "menu"}


def filter_main (call):
    return call.data in [
        "echo", 
        "calc", 
        "guess", 
        "cancel", 
        "photo", 
        "menu", 
        "hack", 
        "yt_search",
        "shop",
        "send_sticker"
    ] 


def filter_echo (message):
    return filter_state (message) and data [message.chat.id] ["state"] == "echo"


def filter_calc (message):
    return filter_state (message) and data [message.chat.id] ["state"] == "calc"


def filter_photo (message):
    return filter_state (message) and data [message.chat.id] ["state"] == "photo"


def filter_diff (call):
    return call.data == "light" or call.data == "medium" or call.data == "hard"


def filter_guess (message):
    return filter_state (message) and data [message.chat.id] ["state"] == "guess"


def filter_hack (call):
    return call.data == "confirm_hack"


def filter_shop (message):
    return filter_state (message) and data [message.chat.id] ["state"] == "shop"


def filter_buy_pineapple (call):
    return call.data == "buy_pineapple"


def filter_buy_dragon_fruit (call):
    return call.data == "buy_dragon_fruit"


def filter_search_yt (message):
    return filter_state (message) and data [message.chat.id] ["state"] == "yt_search"



@bot.message_handler (
    commands=[
        "start", 
        "menu"
    ]
)
def start_message (message):
    data [message.chat.id] = {"state": "start"}
    bot.send_message (
        message.chat.id,
        message.from_user.first_name + MESSAGES [
            "first_appeal_txt"
        ],
        reply_markup=markup
    )
    if os.path.exists ("media.json"):
        with open ("media.json", "r") as file:
            id_s = json.load (file)
    else:
        id_s = {
            "sticker":[],
            "video":[],
            "audio":[]
        }
        with open (patch, "w") as file:
            json.dump (id_s, file)


        
@bot.message_handler (content_types=["sticker"])
def send_sticker_id (message):
    global id_s
    id = message.sticker.file_id
    id_s ["sticker"].append (id)
    with open ("media.json", "w") as file:
        json.dump (id_s, file)
    print (id)
    bot.send_message (message.chat.id, id)


@bot.message_handler (func=filter_file)
def random_file (message):
    global id_s
    try:
        with open ("media.json", "r") as file:
            id_s = json.load (file)
        if message == "Стикер":
            result = id_s ["sticker"] [randint (0, len (id_s ["sticker"]) - 1)]
            bot.send_message (
                message.chat.id,
                result
            )
    except:
        bot.send_message (
            message.chat.id,
            text="Мне ещё ничего не прислали"
        )
    bot.send_message (
        message.chat.id,
        text="Если хочешь вернутся в меню, нажми кнопку",
        reply_markup=cancel_markup
    )


@bot.callback_query_handler (func=filter_main)
def commands (call):
    bot.answer_callback_query (call.id)
    if not call.message.chat.id in data:
        data [call.message.chat.id] = {"state": "menu"}
    else:
        if call.data == "echo":
            data [call.message.chat.id] ["state"] = "echo"
            bot.send_message (
                call.message.chat.id, 
                MESSAGES [
                    "echo_message_txt"
                ]
            )
            
        if call.data == "calc":
            data [call.message.chat.id] ["state"] = "calc"
            bot.send_message (
                call.message.chat.id, 
                MESSAGES [
                    "calc_message_txt"
                ]
            )
            
        if call.data == "cancel":
            data [call.message.chat.id]["state"] = "menu"
            bot.send_message(
                call.message.chat.id, 
                MESSAGES [
                    "menu_message_txt"
                ], 
                reply_markup=markup
            )
            
        if call.data == "photo":
            data [call.message.chat.id] ["state"] = "photo"
            bot.send_photo (
                call.message.chat.id, 
                photo=photos [
                    randint (
                        0, 
                        len (photos) - 1
                    )
                ], 
                reply_markup=more_photo_markup
            )
            
        if call.data == "guess":
            bot.send_message (
                call.message.chat.id, 
                MESSAGES [
                    "guess_message_txt"
                ], 
                reply_markup=selecter_mode_markup
            )

        if call.data == "hack":
            data [call.message.chat.id] ["state"] = "hack"
            bot.send_message (
                call.message.chat.id, 
                "Точно?", 
                reply_markup=confirm_markup
            )
            
        if call.data == "yt_search":
            data [call.message.chat.id] ["state"] = "yt_search"
            bot.send_message (
                call.message.chat.id, 
                "Введи поисковый запрос", 
                reply_markup=cancel_markup
            )

        if call.data == "shop":
            data [call.message.chat.id] ["state"] = "shop"
            bot.send_message (
                call.message.chat.id,
                "Выбери то, что хочешь купить",
                reply_markup=shop_markup
            )

        if call.data == "send_sticker":
            data [call.message.chat.id] ["state"] = "send_sticker"
            bot.send_message (
                call.message.chat.id,
                "Что тебе нада?",
                reply_markup=file_markup
            )



@bot.message_handler (func=filter_calc)
def calculator (message):
    try:
        result = eval (
            message.text.replace (
                "^", 
                "**"
            )
        )
        bot.send_message (
            message.chat.id, 
            "Ответ: " + str (
                result
            ), 
            reply_markup=cancel_markup
        )
    except ArithmeticError:
        bot.send_message (
            message.chat.id, 
            MESSAGES [
                "calc_math_err_txt"
            ], 
            reply_markup=cancel_markup
        )
    except:
        bot.send_message (
            message.chat.id, 
            MESSAGES [
                "unknow_err_txt"
            ], 
            reply_markup=cancel_markup
        )


@bot.message_handler (func=filter_echo)
def echo_message (message):
    answer = message.text
    bot.reply_to (
        message, 
        answer, 
        reply_markup=cancel_markup
    )


@bot.callback_query_handler (func=filter_diff)
def guess_diff (call):
    bot.answer_callback_query (call.id)
    global random_number
    if call.data == "light":
        random_number = randint (0, 10)
        bot.send_message (
            call.message.chat.id, 
            MESSAGES [
                "easy_mode_select_txt"
            ]
        )
    elif call.data == "medium":
        random_number = randint (0, 50)
        bot.send_message (
            call.message.chat.id, 
            MESSAGES [
                "medium_mode_select_txt"
            ]
        )
    elif call.data == "hard":
        random_number = randint (
            0, 
            100
        )
        bot.send_message (
            call.message.chat.id, 
            MESSAGES [
                "hard_mode_select_txt"
            ]
        )
    data [call.message.chat.id] ["state"] = "guess"
    bot.send_message (
        call.message.chat.id, 
        text=MESSAGES [
            "cancel_txt"
        ], 
        reply_markup=cancel_markup
    )


@bot.message_handler (func=filter_guess)
def guess (message):
    try:
        if int (message.text) > random_number:
            bot.send_message (
                message.chat.id, 
                MESSAGES [
                    "guess_num_less_txt"
                ]
            )
        elif int (message.text) < random_number:
            bot.send_message (
                message.chat.id, 
                MESSAGES [
                    "guess_num_more_txt"
                ]
            )
        else:
            bot.send_message (
                message.chat.id, 
                MESSAGES [
                    "guess_num_equally_txt"
                ]
            )
    except ValueError:
        bot.send_message (
            message.chat.id, 
            MESSAGES [
                "value_err_txt"
            ]
        )
    except:
        bot.send_message (
            message.chat.id, 
            MESSAGES [
                "unknow_err_txt"
            ]
        )
    bot.send_message (
        message.chat.id, 
        text=MESSAGES [
            "cancel_txt"
        ], 
        reply_markup=cancel_markup
    )


@bot.callback_query_handler (func=filter_hack)
def hack (call):
    bot.answer_callback_query (call.id)
    for i in range (0, 100):
        try:
            bot.edit_message_text (
                f"Взлом пентагона... {i + randint (0, 1)}%", 
                call.message.chat.id, 
                call.message.message_id
            )
        except:
            pass
        sleep (0.1)
    if randint (0, 2) == 0:
        sleep (1)
        try:
            bot.edit_message_text (
                MESSAGES [
                    "hack_fail_txt"
                ], 
                call.message.caht.id, 
                call.message.message_id
            )
        except:
            pass
    else:
        try:
            bot.edit_message_text (
                MESSAGES [
                    "hack_succ_txt"
                ], 
                call.message.chat.id, 
                call.message.message_id
            )
        except:
            pass
        for i in range (0, 100):
            try:
                bot.edit_message_text(
                    f"Поиск секретных данных об НЛО... {i + randint(0, 1)}%", 
                    call.message.chat.id, 
                    call.message.message_id
                )
            except:
                pass
        sleep (0.1)



@bot.callback_query_handler (func=filter_buy_pineapple)
def buy_pineapple (call):
    bot.answer_callback_query (call.id)
    price = [
        LabeledPrice (
            label="Ананас", 
            amount=249 * 100
        )
    ]
    bot.send_invoice (
        call.from_user.id,
        title="Ананас",
        description=MESSAGES [
            "pineapple_description"
        ],
        provider_token=PROVIDER_TOKEN,
        currency='RUB',
        photo_url="https://fleuramour.ru/wp-content/uploads/4/0/b/40be99547098346f53838d39cec07de3.jpeg",
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=False,
        prices=price,
        start_parameter="start_parameter",
        invoice_payload="coupon",
        max_tip_amount=500 * 100,
        suggested_tip_amounts=(
            50 * 100, 
            150 * 100, 
            250 * 100, 
            500 * 100
        )
    )


@bot.callback_query_handler (func=filter_buy_dragon_fruit)
def buy_dragon_fruit (call):
    bot.answer_callback_query (call.id)
    price = [
        LabeledPrice (
            label="Драгон фрукт",
            amount=549 * 100
        )
    ]
    bot.send_invoice (
        call.from_user.id,
        title="Драгон фрукт",
        description=MESSAGES [
            "dragon_fruit_description"
        ],
        provider_token=PROVIDER_TOKEN,
        currency='RUB',
        photo_url="https://orchidea-shop.ru/base/data/6664mid.jpg",
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=False,
        prices=price,
        start_parameter="start_parameter",
        invoice_payload="coupon",
        max_tip_amount=500 * 100,
        suggested_tip_amounts=(
            50 * 100,
            150 * 100,
            250 * 100,
            500 * 100
        )
    )



@bot.pre_checkout_query_handler (func=lambda query: True)
def process_pre_checkout_query (pre_checkout_query: types.PreCheckoutQuery):
    print (pre_checkout_query.id)
    print (pre_checkout_query.total_amount)
    print (pre_checkout_query.from_user)
    bot.answer_pre_checkout_query (
        pre_checkout_query.id, 
        ok=True
    )


@bot.message_handler (
    content_types=[
        'successful_payment'
    ]
)
def process_successful_payment (message):
    bot.send_photo (
        message.chat.id, 
        photo="https://transonlain.ru/wp-content/uploads/2021/07/платеж-прошел-1536x1086.png", 
        caption=MESSAGES[
            "successful_payment_txt"
        ]
    )
    

@bot.message_handler (func=filter_search_yt)
def get_vdeo (message):
    global url, regexp, pattern
    query_string = urllib.parse.urlencode ({"search_query" : message.text})
    res = req.get (url + query_string)
    if res.ok:
        body = res.text
        links = pattern.findall (body) [:2]
        for link in links:
            answer = "https://www.youtube.com/watch?v=" + link
            bot.send_message (
                message.from_user.id,
                answer
            )
        bot.send_message (
            message.chat.id, 
            text=MESSAGES [
                "cancel_txt"
            ], 
            reply_markup=cancel_markup
        )


if __name__ == "__main__":
    bot.polling (non_stop=True)  # Рабочий цикл бота
 
