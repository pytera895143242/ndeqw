from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import sqlite3
import random


from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN
import text_or_question as text
import keaboard as kb
import time
import datetime
import asyncio

from db_admin import DateBase

from sqlit import reg_user,obnova_members_status,count_member_in_status,info_members,send_status_no_rassilka,cheack_status,finish_bot,cheack_finish

datebase = DateBase('users.db')

bot = Bot(token=TOKEN,parse_mode='html')
db = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()
    step_q = State()
    step_regbutton = State()

class Form(StatesGroup):
    info_text = State()
    user_delete = State()

class reg_step(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
    step4 = State()
    step5 = State()




ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 678623761 #Бекир
ADMIN_ID_4 = 941730379 #Джейсон
ADMIN_ID_5 = 807911349 #Байзат
ADMIN_ID_6 = 1045832338 #Коля 2 (НИКОЛА_ОДНОУС)

ADMIN = [ADMIN_ID_1,ADMIN_ID_2,ADMIN_ID_3,ADMIN_ID_4,ADMIN_ID_5,ADMIN_ID_6]

user_1 = '@nikolanext' #ДЛЯ ТЕХ, КТО ПЛАТНЫЙ (1)
user02349 = '@NikolaOdnous' #ДЛЯ ТЕХ, КТО НЕ (1)

@db.message_handler(commands=['start'])
async def greetings(message: types.Message):

    user_id = message.chat.id
    reg_user(user_id,0,0) #Записываем в базу человека со статусом 0

    m = await message.answer_photo(text.hi_photo_id, caption=text.hi_text, reply_markup=kb.the_first_go_button)

    go_new = 'Г'
    for i in range(1,14):
        go_new+='о'
        await bot.edit_message_caption(chat_id=user_id,message_id=m.message_id,caption=text.hi_text.format(go_new),reply_markup=kb.the_first_go_button)
        await asyncio.sleep(0.43)



@db.message_handler(commands=['admin'],state='*')
async def vienw_adminka(message: types.Message,state: FSMContext):
    await state.finish()
    if message.chat.id in ADMIN:
        button1 = KeyboardButton('📊Статистика всех пользователей')

        button2 = KeyboardButton('💿База данных')
        button3 = KeyboardButton('🔫Удаление челов')

        button4 = KeyboardButton('👶Рассылка молодым')
        button5 = KeyboardButton('👴Рассылка Старикам')

        markup3 = ReplyKeyboardMarkup(resize_keyboard=True)
        markup3 = markup3.add(button1)
        markup3 = markup3.add(button2,button3)
        markup3 = markup3.add(button4,button5)

        await bot.send_message(chat_id=message.chat.id,text='Открыта админка 🔘',reply_markup=markup3)





@db.message_handler(state=Form.user_delete,content_types=['video','voice','photo','video_note','file','document','text'])
async def delete_user(message: types.Message, state: FSMContext):
    try:
        user_id = message.forward_from.id
        send_status_no_rassilka(user_id)
    except Exception as e:
        print(e)

    markup = types.InlineKeyboardMarkup()
    bat_otmena12 = types.InlineKeyboardButton(text='Выйти из режима удаления',callback_data='exit_del')
    markup.add(bat_otmena12)

    await message.answer('Пользователь удалён 🩸',reply_markup=markup)

@db.callback_query_handler(text = 'five_question', state = reg_step.step1)
async def answer_push_inline_button(call, state: FSMContext):
    q = int((await state.get_data())['time'])
    if q == 1:
        await call.message.answer_animation(text.the_first_question_gif_id, caption=text.the_first_question_text,reply_markup=kb.first_question_buttons)
    else:
        await bot.send_message(chat_id=call.message.chat.id,text="""Аяяй я смотрю, кто-то решил
пошалить 😏

Сначала смотри кругляш, а потом нажимай))👌""")

@db.message_handler(state= reg_step.step2 ,content_types=['text'])
async def domasha_link(message: types.Message, state: FSMContext):
    if message.text[0] == '@' or message.text[0:12] == "https://t.me" or message.text[0:11] == "http://t.me" or message.text[0:4]== 't.me':
        await state.update_data(ready=1)  # Выключает прогрев
        await bot.send_video(video='BAACAgIAAxkBAAOUYXKv7FeERpaKhIC7y1eZpgQM3BsAAjAPAAL4PZlLKFIGbCge7s4hBA',chat_id=message.chat.id)
        await reg_step.step3.set()

    else:
        await bot.send_message(chat_id=message.chat.id,text="""Неправильно указана ссылка на канал! 

Должно быть:
Или так - https://t.me/ канал  
Или так - @ канал 
Как показано на видео!""")


@db.message_handler(state= reg_step.step3 ,content_types=['text'])
async def domasha_test(message: types.Message, state: FSMContext):
    if message.text == 'Тест' or message.text == 'тест':
        markup = InlineKeyboardMarkup(row_width=4)
        bat1 = InlineKeyboardButton('К', callback_data='finish_sprint')
        bat2 = InlineKeyboardButton('А', callback_data='continue_sprint')
        bat3 = InlineKeyboardButton('Й', callback_data='finish_sprint')
        bat4 = InlineKeyboardButton('Ф', callback_data='finish_sprint')
        markup.add(bat1,bat2,bat3,bat4)

        await message.answer_animation(animation='CgACAgIAAxkBAAOyYXK4yClI4-unzjZxyX277VQFRCUAAsgKAALOVCBIdPqdFCjI3u4hBA',caption="""<b>Что такое трафик?</b>

<b>К)</b> Количество человек в директе.

<b>А)</b> Количество пользователей, которые за единицу времени, перешли на сайт.

<b>Й)</b> Количество подписчиков.

<b>Ф)</b> Название чипсов, у того лысого мужика.""",reply_markup=markup)
        await state.finish()




@db.message_handler(state= reg_step.step4 ,content_types=['text'])
async def domasha_test(message: types.Message, state: FSMContext):
    if message.text == 'Кино' or message.text == 'кино':
        await state.update_data(ready1=1)  # Выключает прогрев
        markup = InlineKeyboardMarkup()
        bat1 = InlineKeyboardButton('Вперёд 🤜💥', callback_data='vpered')
        markup.add(bat1)
        await bot.send_video_note(chat_id=message.chat.id,video_note='DQACAgIAAxkBAAPsYXLDT0bUolS7QGQwXdDC1jcvjwYAAvQPAAL4PZlLgRpefoFjEN8hBA',reply_markup=markup)

        await state.update_data(time = 0)
        await asyncio.sleep(30)#30
        await state.update_data(time = 1)


#####
########
#########################################################
@db.callback_query_handler(text='otemena',state='*')
async def otmena_12(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()
    try:
        await bot.delete_message(call.message.chat.id,message_id=call.message.message_id)
    except: pass


@db.message_handler(state=st_reg.step_q,content_types=['text','photo','video','video_note','animation','voice','sticker']) # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    await st_reg.st_name.set()
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
    bat2 = types.InlineKeyboardButton(text='Добавить кнопки', callback_data='add_but')
    murkap.add(bat1)
    murkap.add(bat2)
    murkap.add(bat0)

    await message.copy_to(chat_id=message.chat.id)
    q = message
    await state.update_data(q=q)

    await bot.send_message(chat_id=message.chat.id,text='Пост сейчас выглядит так 👆',reply_markup=murkap)


# НАСТРОЙКА КНОПОК
@db.callback_query_handler(text='add_but',state=st_reg.st_name) # Добавление кнопок
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id,text='Отправляй мне кнопки по принципу Controller Bot\n\n'
                                                     'Пока можно добавить только одну кнопку')
    await st_reg.step_regbutton.set()
    await bot.answer_callback_query(callback_query_id=call.id)

@db.message_handler(state=st_reg.step_regbutton,content_types=['text']) # Текст кнопок в неформате
async def redarkt_button(message: types.Message, state: FSMContext):
    arr2 = message.text.split('-')

    k = -1  # Убираем пробелы из кнопок
    for i in arr2:
        k+=1
        if i[0] == ' ':
            if i[-1] == ' ':
                arr2[k] = (i[1:-1])
            else:
                arr2[k] = (i[1:])

        else:
            if i[-1] == ' ':

                arr2[0] = (i[:-1])
            else:
                pass

    # arr2 - Массив с данными


    try:
        murkap = types.InlineKeyboardMarkup() #Клавиатура с кнопками
        bat = types.InlineKeyboardButton(text= arr2[0], url=arr2[1])
        murkap.add(bat)

        data = await state.get_data()
        mess = data['q']  # ID сообщения для рассылки

        await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,message_id=mess.message_id,reply_markup=murkap)

        await state.update_data(text_but =arr2[0]) # Обновление Сета
        await state.update_data(url_but=arr2[1])  # Обновление Сета

        murkap2 = types.InlineKeyboardMarkup() # Клавиатура - меню
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
        murkap2.add(bat1)
        murkap2.add(bat0)

        await bot.send_message(chat_id=message.chat.id,text='Теперь твой пост выглядит так☝',reply_markup=murkap2)


    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()

# КОНЕЦ НАСТРОЙКИ КНОПОК


@db.callback_query_handler(text='send_ras',state="*") # Рассылка
async def fname_step(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

    data = await state.get_data()
    mess = data['q'] # Сообщения для рассылки

    type_rass = data['type_rassilki']
    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками

    try: #Пытаемся добавить кнопки. Если их нету оставляем клаву пустой
        text_but = data['text_but']
        url_but = data['url_but']
        bat = types.InlineKeyboardButton(text=text_but, url=url_but)
        murkap.add(bat)
    except: pass


    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    if type_rass == 120:
        users = sql.execute(f"SELECT id FROM user_time WHERE status_active = 1 or status_active = 2").fetchall()
    else:
        users = sql.execute(f"SELECT id FROM user_time WHERE status_active = 3 or status_active = 4").fetchall()

    bad = 0
    good = 0
    xz_bad = 0

    await bot.send_message(call.message.chat.id, f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        if (cheack_finish(i[0]))[0] == 1:
            await asyncio.sleep(0.1)
            try:
                await mess.copy_to(i[0],reply_markup=murkap)
                good += 1
            except:
                bad += 1

        else:
            xz_bad+=1
    await bot.send_message(chat_id = call.message.chat.id,text=
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не дошли до конца (не отправленно):</b> <code>{xz_bad}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>"
    )
#########################################################
########
#####

@db.callback_query_handler(text='dalee2',state=reg_step.step5) #Последний хендлер
async def lasthandler_dalle2(call: types.callback_query, state: FSMContext):
    go_progrev = ((await state.get_data())['go_progrev'])

    if go_progrev == 0: #Защита от повторного прохождения
        await state.update_data(go_progrev = 1)

        status = int((cheack_status(call.message.chat.id))[0])

        if status == 1 or status == 2: #Молодняк
            if int((cheack_status(call.message.chat.id))[0]) !=9:
                await bot.send_video(chat_id=call.message.chat.id,video='BAACAgIAAxkBAAID3WF07KUvuu4TTtrRILBByH9tx1R0AALLEAACSjepSxiIfsnDPHmjIQQ',caption="""@NikolaOdnous""")
            finish_bot(call.message.chat.id)
            await asyncio.sleep(random.randint(43200-3600,43200+3600))#43200 сек - 12 часов

            if int((cheack_status(call.message.chat.id))[0]) != 9:
                await bot.send_photo(
                    photo='AgACAgIAAxkBAAEEybxhplvXSh6AcHkCQJgBoH5m0_aCpgACCrcxGy7EIElViimNbd5rWgEAAwIAA3MAAyIE',
                    chat_id=call.message.chat.id, caption="""🔥Осталось 2 места, по скидке🔥

Мишаня, <b>сделал почти 100$ за день</b>, примерно 4 месяца назад, он попал в спринт, полным нулём)

И рассказывал, как <b>устал зависеть от родаков!</b>

Как ему <b>стыдно просить деньги</b>, и хочется самостоятельно, себя обеспечивать!

Не понимаю подростков, есть телефон, есть интернет, а они не пользуются этим 🤧

Задумайся☝️ мы ещё готовы помочь тебе, начать зарабатывать в интернете.

<b>Вперёд</b> 🤘 @NikolaOdnous""")

            await asyncio.sleep(43200/2)#6 часов (43.200/2)
            if int((cheack_status(call.message.chat.id))[0]) != 9:
                await bot.send_video(chat_id=call.message.chat.id,video='BAACAgIAAxkBAAEEydVhpmASbuFaevJLDPEb-wumlc3YWAACORMAAi7EIEn53-xGzUZaySIE',caption="""Ааааа🙀 10.6 🍋🍋🍋

<b>Просто глянь, видосик 😎</b>

Тяжело передать насколько я в афиге от нашей движухи, но это просто разнос!

<b>Не упускай, действуй, зарабатывай!</b>

Вливайся 💪 @NikolaOdnous""")

            await asyncio.sleep(random.randint(43200-3600,43200+3600))#43200 сек - 12 часов
            if int((cheack_status(call.message.chat.id))[0]) != 9:
                await bot.send_photo(
                chat_id=call.message.chat.id,
                photo='AgACAgIAAxkBAAIB-GF0PGOruGuGcsFaHnGe8e8vLF4AAyS2MRuCdZlLl3qXGTVeAAFwAQADAgADeAADIQQ',
                caption="""<b>30$ за вечер🔥</b>

Согласись неплохо? Учитывая, что это без образования, и похода на некайфовую работу 🤮

<b>Бабки = свобода</b>
Делать то что ты хочешь, и брать от жизни максимум, особенно пока ты молод!

Куча ребят сидят 
без денег, и думают что 
все впереди 🤣

❗️Сейчас надо рубить капусту, сейчас получай максимальное удовольствие от жизни.

А потом уже будет поздно, <b>послушай мой подкаст, и поймёшь, о чем я </b>👇
https://t.me/rilttok/199""")

            await asyncio.sleep(random.randint(43200-3600,43200+3600))#43200 сек - 12 часов
            if int((cheack_status(call.message.chat.id))[0]) != 9:
                await bot.send_photo(
                chat_id=call.message.chat.id,
                photo='AgACAgIAAxkBAAEEydthpmHZvQV2K80FnV7w3i-QnSCTdgACNbcxGy7EIElp5XcXdh2oaAEAAwIAA3MAAyIE',
                caption="""<b>33 доллара за 2 часа, ну что за 
тигр 🐅</b>

Телега сейчас на пике прибыльности, и простоты)

Это факт, который ясен не многим, зачем искать подработку, если есть Телеграм под носом!

Моё предложение, раскрутить свой канал без вложений, все ещё в силе!

Хватит быть массой, пошли в 
команду, зарабатывать 
по кайфу💰 

👉 @NikolaOdnous""")

            await asyncio.sleep(random.randint(43200-3600,43200+3600))#43200 сек - 12 часов
            if int((cheack_status(call.message.chat.id))[0]) != 9:
                await bot.send_photo(
                chat_id=call.message.chat.id,
                photo='AgACAgIAAxkBAAEEydxhpmIo8n4DiB92LLigOjvbMv9nzAACEbcxGy7EIEnNaJUEls8idQEAAwIAA3MAAyIE',
                caption="""<b>67$ как с пола подобрать!</b>

- Кто то батрачит, а кто то заливает ролики в тик ток 😎

- Кто то ноет как все плохо, а кто то уже начал действовать!

- Кто то читает этот текст, а кто то уже помогает семье, и растит свой канал!

А что выберешь ты? 

1) Газ в пол 🚘 @NikolaOdnous
2) Упустить последний шанс!""")

        else:
            if int((cheack_status(call.message.chat.id))[0]) != 9:
                await bot.send_video(chat_id=call.message.chat.id,
                                     video='BAACAgIAAxkBAAID3mF07K3RtGxIH1fXZqle4FBCuCDsAALMEAACSjepS7WX561dG_u0IQQ',
                                     caption="""@nikolanext""")
            finish_bot(call.message.chat.id)
            await asyncio.sleep(random.randint(43200 - 3600, 43200 + 3600))  # 43200 сек - 12 часов


            if int((cheack_status(call.message.chat.id))[0]) != 9:
                await bot.send_photo(photo='AgACAgIAAxkBAAEEyd1hpmLOePOVZZg911LuCLQIo8AtywACCrcxGy7EIElViimNbd5rWgEAAwIAA3MAAyIE',chat_id=call.message.chat.id,caption="""🔥Осталось 2 места, по скидке🔥

Мишаня, <b>сделал почти 100$ за день</b>, примерно 4 месяца назад, он попал в спринт, полным нулём)

Рассказывал, как ему трудно, постоянно нахватает денег, бесконечные кредиты, гавнистая работа!

На самом деле, в наше время, имея телефон, имея интернет, глупо не подрабатывать онлайн!

У тебя есть всё. Чтобы зарабатывать в интернете, не упускай шанс!

Задумайся☝️ мы ещё готовы помочь тебе разобраться) 

<b>Вперёд</b> 🤘@nikolanext""")

            await asyncio.sleep(random.randint(43200/2))  # 6 часов (43.200/2)
            if int((cheack_status(call.message.chat.id))[0]) != 9:
                await bot.send_video(chat_id=call.message.chat.id,
                                     video='BAACAgIAAxkBAAEEyephpmO22NmAeZVX1O6EKQYPhYCzDwACORMAAi7EIEn53-xGzUZaySIE',
                                     caption="""Ааааа🙀 <b>10.6</b> 🍋🍋🍋

<b>Просто глянь, видосик 😎</b>

Тяжело передать насколько я в афиге от нашей движухи, но это просто разнос!

<b>Не упускай, действуй, зарабатывай!</b>

Вливайся 💪 @nikolanext""")

        await asyncio.sleep(random.randint(43200 - 3600, 43200 + 3600))  # 43200 сек - 12 часов
        if int((cheack_status(call.message.chat.id))[0]) != 9:
            await bot.send_photo(chat_id=call.message.chat.id,
                                 photo='AgACAgIAAxkBAAEEyexhpmRk8ap4kRSkWgigCz2OYAItuAACEbcxGy7EIEnNaJUEls8idQEAAwIAA3MAAyIE',
                                 caption="""<b>67$ как с пола подобрать!</b>

- Кто то батрачит, а кто то заливает ролики в тик ток 😎

- Кто то ноет как все плохо, а кто то уже начал действовать!

- Кто то читает этот текст, а кто то уже помогает семье, и растит свой канал!

А что выберешь ты? 

1) Газ в пол  🚘 @nikolanext
2) Упустить возможность!""")

        await asyncio.sleep(random.randint(43200 - 3600, 43200 + 3600))  # 43200 сек - 12 часов
        if int((cheack_status(call.message.chat.id))[0]) != 9:
            await bot.send_photo(chat_id=call.message.chat.id,
                                 photo='AgACAgIAAxkBAAEEye5hpmS0cfhRvRRGtHjiZhHFeqLdbAACNbcxGy7EIElp5XcXdh2oaAEAAwIAA3MAAyIE',
                                 caption="""<b>33 доллара за 2 часа🙀</b>

Телега сейчас на пике прибыльности, и простоты)

Это факт, который ясен не многим, зачем искать подработку, если есть Телеграм под носом!

Моё предложение, раскрутить свой канал без вложений, все ещё в силе!

Хватит быть массой, пошли в 
команду, зарабатывать 
по кайфу💰 

👉 @nikolanext""")

        await asyncio.sleep(random.randint(43200 - 3600, 43200 + 3600))  # 43200 сек - 12 часов
        if int((cheack_status(call.message.chat.id))[0]) != 9:
            await bot.send_photo(chat_id=call.message.chat.id,
                                 photo='AgACAgIAAxkBAAEEye9hpmT6O6Sm3UPPC0be6JGZhRDVtwACQLcxGy7EIEnu45dd1RdCWgEAAwIAA3MAAyIE',
                                 caption="""<b>30$ за вечер)</b>

Команда не может не радовать результатами 😎

Кстати, мы полностью обновили обучение, добавили новые фишки, о которых никто не знает 🤫

Тик ток стал очень жёстким, без вложений раскрутить канал, становится все сложнее, и сложнее!

Чем дольше ждёшь, тем труднее сделать результат!

Начинай сейчас, чтобы потом не пожалеть 🤜 @nikolanext""")



@db.callback_query_handler(lambda call: True, state = '*')
async def answer_push_inline_button(call, state: FSMContext):
    user_id = call.message.chat.id # ЮЗЕР ЧЕЛА
    status = (cheack_status(user_id))[0]
    if status == 1:
        username_contact = user_1
    else:
        username_contact = user02349

    if call.data == 'exit_del':
        await state.finish()
        await bot.send_message(chat_id=call.message.chat.id,text='Отменено. Включен обычный режим✅')

    if call.data == 'go_button':
        await call.message.answer_video_note(text.video_note_id, reply_markup=kb.pass_the_five_question)
        await reg_step.step1.set()
        await state.update_data(time = 0) # Заглушка
        await asyncio.sleep(30) #30
        await state.update_data(time = 1) #Чел досмотрел видео

    elif call.data[0:14] == 'first_question':
        await call.message.delete()

        if call.data == 'first_question1': # Группа 1 (до 14)
            obnova_members_status(call.message.chat.id, 1)
        if call.data == 'first_question2': # Группа 1 (15-19)
            obnova_members_status(call.message.chat.id, 2)
        if call.data == 'first_question3': # Группа 2 (20-30)
            obnova_members_status(call.message.chat.id, 3)
        if call.data == 'first_question4': # Группа 2 (31-102)
            obnova_members_status(call.message.chat.id, 4)

        await call.message.answer_animation(text.the_second_question_gif_id, caption=text.the_second_question_text,
                                            reply_markup=kb.second_question_buttons)
    elif call.data == 'second_question':
        await call.message.delete()
        await call.message.answer_animation(text.the_third_question_gif_id, caption=text.the_third_question_text,
                                            reply_markup=kb.third_question_buttons)
    elif call.data == 'third_question':
        await call.message.delete()
        await call.message.answer_animation(text.the_fourth_question_gif_id, caption=text.the_fourth_question_text,
                                            reply_markup=kb.fourth_question_buttons)


    elif call.data[:15] == 'fourth_question':
        await call.message.delete()
        await call.message.answer_animation(text.the_five_question_gif_id, caption=text.the_five_question_text,
                                            reply_markup=kb.five_question_buttons)




    elif call.data == 'five_questions':
        await call.message.delete()
        await call.message.answer("""<b>🕺🏻А вот и подгон от Одноуса🕺🏻</b>

🔻 За успешное прохождение 🔻""")
        await call.message.answer_document(text.bonus_dock_file_id)
        await call.message.answer_photo(text.finished_text_file_id, caption=text.finished_text, reply_markup=kb.finished_text_button)

    elif call.data == 'go_2':
        await call.message.answer_video('BAACAgIAAxkBAANjYXKph4KoOVzcRJlbcCqIBZLAxCIAAisQAAIMP5lLtZKH8w_RzVAhBA',caption="""После выполнения Д/З 
Ты получишь следующее видео!

Если возникнут трудности, с выполнением Д/З, то пиши мне в Инстаграм)

💪 https://instagram.com/nikolanext""") ##ДОМАШКА (ССЫЛКА)
        await reg_step.step2.set()

        await state.update_data(ready = 0)

        try :
            int((await state.get_data())['proverka'])
        except:
            await state.update_data(proverka=0)
            await state.update_data(proverka=1)  # Не допускает запуск повторного прогрева
            await asyncio.sleep(900)  # 900

            if int((await state.get_data())['ready']) == 0:  # Прогрев через первые 15 минут
                await bot.send_message(chat_id=call.message.chat.id,
                                       text="""Прошло 15 минут, я жду твоё домашнее задание 🤗""")

                await asyncio.sleep(900)  # 900
                if int((await state.get_data())['ready']) == 0:  # Прогрев через 30 минут
                    await bot.send_message(chat_id=call.message.chat.id, text="""Вай вай 30 минут прошло, а от тебя, ни слуху, ни духу, давай скорей погнали дальше, я жду 😎
        
Если возникли сложности, с д/з напиши мне в Инстаграм☝️""")
                await asyncio.sleep(86400)  # 86400
                if int((await state.get_data())['ready']) == 0:  # Прогрев через 24 часа
                    while int((await state.get_data())['ready']) == 0:
                        await call.message.answer_video(
                            'BAACAgIAAxkBAANjYXKph4KoOVzcRJlbcCqIBZLAxCIAAisQAAIMP5lLtZKH8w_RzVAhBA', caption="""После выполнения Д/З 
Ты получишь следующее видео!

Если возникнут трудности, с выполнением Д/З, то пиши мне в Инстаграм)

💪 https://instagram.com/nikolanext""")
                        await asyncio.sleep(86400)  # 86400


    elif call.data == 'finish_sprint':
        await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,text= """Ну что же ты так, надо было внимательно смотреть видео!

Теперь все, спринт для тебя закончился!""")

    elif call.data == 'continue_sprint':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_video(video='BAACAgIAAxkBAAPXYXK9E6cAAWAF3hDj-_XBMPVjtZJEAAJ6DwAC-D2ZS76E98_wTJl0IQQ',chat_id=call.message.chat.id)
        await reg_step.step4.set() #Ожидает слово "Кино"

        await state.update_data(ready1=0)

        try:
            int((await state.get_data())['proverka1'])
        except:
            await state.update_data(proverka1=1)  # Не допускает запуск повторного прогрева
            await asyncio.sleep(900)  # 900

            if int((await state.get_data())['ready1']) == 0:  # Прогрев через первые 15 минут
                await bot.send_message(chat_id=call.message.chat.id,text= """Прошло 15 минут, я жду когда ты напишешь это слово 😉

Скорей смотри видео☝️""")
                await asyncio.sleep(900) # 900
                if int((await state.get_data())['ready1']) == 0:  # Прогрев 30 минут
                    await bot.send_message(chat_id=call.message.chat.id, text="""Прошло 30 минут, тебе не интересно начать зарабатывать? 

Скорей смотри видео, и пиши это слово☝️""")
                    await asyncio.sleep(1800)#1800
                    if int((await state.get_data())['ready1']) == 0:  # Прогрев 1 час:
                        await bot.send_message(chat_id=call.message.chat.id,text="""Через 24 часа, ты не сможешь узнать, как начать зарабатывать!

Это последнее сообщение, скорей смотри видео, и пиши это слово!""")

    elif call.data == 'vpered':
        if int((await state.get_data())['time']) == 0:
            await bot.send_message(chat_id=call.message.chat.id,text = """Аяяй я смотрю, кто-то решил
пошалить 😏

Сначала смотри кругляш, а потом нажимай))👌""")
        else:
            await state.finish()

            markup = InlineKeyboardMarkup()
            bat1 = InlineKeyboardButton('💥 Далее 💥', callback_data='dalee1')
            markup.add(bat1)

            v0 = await bot.send_video(chat_id=call.message.chat.id,video='BAACAgIAAxkBAAPtYXLh6HJOQbRYbSVYNcOQI1YnwCgAAskPAALV8iFKmRDT1O5tR5YhBA')
            await asyncio.sleep(75)#75 сек
            await bot.edit_message_caption(chat_id=v0.chat.id,reply_markup=markup,message_id=v0.message_id)

###
    elif call.data == 'dalee1':
        markup = InlineKeyboardMarkup()
        bat1 = InlineKeyboardButton('💥 Спринт 💥', callback_data='dalee2')
        markup.add(bat1)

        v7 = await bot.send_video(call.message.chat.id,video='BAACAgIAAxkBAAPuYXLifypzf62YPMgTsMbd-qzXK50AAogVAALalClKfdfg4lvQ5ykhBA')
        await asyncio.sleep(146)#146
        await bot.edit_message_caption(chat_id=v7.chat.id,reply_markup=markup,message_id=v7.message_id)


        await reg_step.step5.set()
        await state.update_data(go_progrev = 0)


    await bot.answer_callback_query(callback_query_id=call.id)
###




@db.message_handler(content_types=['text', 'photo', 'video_note', 'animation', 'document', 'video','file'])
async def all_message(message: types.Message, state: FSMContext):
    # try:
    #     print(message.video.file_id)
    # except:
    #     pass
    #
    # try:
    #     print(message.photo[0].file_id)
    # except:
    #     pass
    #
    # try:
    #     print(message.video_note.file_id)
    # except:
    #     pass
    #
    # try:
    #     print(message.animation.file_id)
    # except:
    #     pass
    #
    # try:
    #     print(message.document.file_id)
    # except:
    #     pass


    if message.chat.id in ADMIN:
        if message.text == '📊Статистика всех пользователей':
            all = info_members()# Всего пользователей
            s1 = count_member_in_status(1)
            s2 = count_member_in_status(2)
            s3 = count_member_in_status(3)
            s4 = count_member_in_status(4)

            s0 = count_member_in_status(0) #Еще не выбрпали ответ
            await bot.send_message(chat_id=message.chat.id,text=f"""<b>👥Всего пользователей: {all}</b>

1️⃣До 14 лет: {s1}
2️⃣15 - 19 лет : {s2}
3️⃣20 - 30 лет: {s3}
4️⃣31 - 102 лет: {s4}

🟡Еще не выбрали ответ: {s0}""",parse_mode='html')

        if message.text == '💿База данных':
            await message.answer_document(open("server.db", "rb"))

        if message.text == '🔫Удаление челов':
            await message.answer('👺Включен режим удаление челов \n'
                                 '🔙Для выхода, напиши "отмена"')
            await Form.user_delete.set()

        if message.text == '👶Рассылка молодым': #Рассылка по группе 1,2,0
            murkap = types.InlineKeyboardMarkup()
            bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
            murkap.add(bat0)
            await bot.send_message(message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем молодым',
                                   reply_markup=murkap)
            await st_reg.step_q.set()

            await state.update_data(type_rassilki = 120) # ТИП расслыки по 1,2,0 группе

        if message.text == '👴Рассылка Старикам': #Рассылка по группе 3,4
            murkap = types.InlineKeyboardMarkup()
            bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
            murkap.add(bat0)
            await bot.send_message(message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем старикам',
                                   reply_markup=murkap)
            await st_reg.step_q.set()

            await state.update_data(type_rassilki= 34) # ТИП расслыки по 3,4 группе


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(db,skip_updates=True)
