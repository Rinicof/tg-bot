# https://github.com/Rinicof/tg-bot
import telebot as tb
from random import randint

data = {}
photos = [
    'https://media.realitatea.net/multimedia/image/202108/w1920/urs-ursulet-pui-de-urs-salvat-1_8b225a3799.jpg', # Медведь
    'https://avatars.mds.yandex.net/get-zen_doc/3957666/pub_5fb385ea268198734de4bb7a_5fb38690268198734de5ece0/scale_1200', # Морская свинка
    'https://4lapki.com/wp-content/uploads/2020/10/Screenshot_7-1.jpg', # Корги
    'https://mirpozitiva.ru/wp-content/uploads/2019/11/1502876242_beautiful-horse_1.jpg', # Конь
    'https://avatars.mds.yandex.net/get-zen_doc/230865/pub_5c3ca3ef6d724700ab2e1720_5c3ca49832639b00ad039247/scale_1200', # Торнадо
    'https://oir.mobi/uploads/posts/2021-04/1619642229_60-oir_mobi-p-severnii-morskoi-kotik-zhivotnie-krasivo-f-65.jpg', # Морской китик
    'https://i12.fotocdn.net/s105/4391b87f2a98ab88/public_pin_l/2240125757.jpg', # Слонёнок
    'https://i.pinimg.com/originals/4f/59/4a/4f594a26e903d996723dc75886e27019.jpg', # Ёжик
    'https://i.pinimg.com/originals/df/31/c9/df31c9819dc91f757cf348669be6f56a.jpg', # Олень
    'https://animalinfo.ru/wp-content/uploads/2021/11/s1200.jpg', # Куница
    'https://fotovmire.ru/wp-content/uploads/2019/03/10152/morda-cherepahi-krupnym-planom-na-fone-korralovyh-rifov.jpg', # Черепаха
    'https://imperia-jilstroy.ru/wp-content/uploads/2019/03/neshvill-_1_.jpg' # Дом
]
TOKEN = '5419028605:AAGqsiNXXiipMlszQs97Sv-tTkf4EDxBi0E'
bot = tb.TeleBot(TOKEN)

cancel_markup = tb.types.InlineKeyboardMarkup()
cancel_btn = tb.types.InlineKeyboardButton('◀️ Назад', callback_data='cancel')
cancel_markup.add(cancel_btn)

markup = tb.types.InlineKeyboardMarkup()
btn_echo = tb.types.InlineKeyboardButton('💭 Эхо-бот', callback_data='echo')
btn_calc = tb.types.InlineKeyboardButton('🔢 Калькулятор', callback_data='calc')
btn_photo = tb.types.InlineKeyboardButton('📸 Фото', callback_data='photo')
markup.add(btn_echo)
markup.add(btn_calc)
markup.add(btn_photo)

more_photo_markup = tb.types.InlineKeyboardMarkup()
more_photo_btn = tb.types.InlineKeyboardButton('🔁 Ещё', callback_data='photo')
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
            bot.send_photo(call.message.chat.id, photo=photos[randint(0, len(photos) - 1)], reply_markup=more_photo_markup)
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
