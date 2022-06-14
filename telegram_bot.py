from datetime import datetime

import telebot
from telebot import types
from telebot.types import InlineKeyboardButton

from config import SEPARATE_SYMBOL, SECRET_KEY
from nbc import NaiveBayesClassifiers
from process_data import ProcessData

bot = telebot.TeleBot(SECRET_KEY)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
        Начало работы
    :param message:
    """

    ProcessData.create_user_state(message.from_user.id)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Зарегистрироваться", callback_data='sign_up'))
    keyboard.add(InlineKeyboardButton("Продолжить анонимно", callback_data='anonymous'))
    bot.send_message(message.chat.id, 'Добро пожаловать новый пользователь.\nСперва давайте познакомимся',
                     reply_markup=keyboard)

    ProcessData.set_current_comm(message.from_user.id, 'sign_up')
    ProcessData.set_current_state(message.from_user.id, 1)


@bot.message_handler(commands=['sign_up'])
def send_welcome(message):
    """
        Регистрация
    :param message:
    """
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Зарегистрироваться", callback_data='sign_up'))
    keyboard.add(InlineKeyboardButton("Продолжить анонимно", callback_data='anonymous'))
    bot.send_message(message.chat.id, 'Давайте познакомимся',
                     reply_markup=keyboard)

    ProcessData.set_current_comm(message.from_user.id, 'sign_up')
    ProcessData.set_current_state(message.from_user.id, 1)


@bot.callback_query_handler(func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'sign_up' and
                                                 ProcessData.get_current_state(message.from_user.id) == 1)
def sign_up(message):
    if message.message:
        if message.data == "sign_up":
            ProcessData.set_current_state(message.from_user.id, 2)
            bot.send_message(message.message.chat.id, 'Укажите ваш год рождения. Используйте формат dd/mm/yyyy')
        elif message.data == "anonymous":
            ProcessData.set_current_comm(message.from_user.id, '')
            ProcessData.set_current_state(message.from_user.id, 0)
            bot.send_message(message.message.chat.id, 'Очень жалко, что вы не хотите познакомиться')
            bot.send_message(message.message.chat.id, '😭')
            bot.send_message(message.message.chat.id, 'Надеюсь вы вернетесь к этому позднее')


@bot.message_handler(func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'sign_up' and
                                          ProcessData.get_current_state(message.from_user.id) == 2)
def get_date_of_birth(message):
    try:
        date_of_birth = datetime.strptime(message.text, '%d/%m/%Y')
        ProcessData.create_new_user(message.from_user.id, date_of_birth)
        ProcessData.set_current_state(message.from_user.id, 3)
        bot.send_message(message.chat.id, 'Укажите ваш город проживания')
    except ValueError:
        bot.send_message(message.chat.id, "Введенна дата, которая не соответствует формату, повторите еще раз")


@bot.message_handler(func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'sign_up' and
                                          ProcessData.get_current_state(message.from_user.id) == 3)
def get_city(message):
    city = message.text
    ProcessData.update_city_user(message.from_user.id, city)
    ProcessData.set_current_state(message.from_user.id, 4)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Мужской", callback_data='male'))
    keyboard.add(InlineKeyboardButton("Женский", callback_data='female'))
    bot.send_message(message.chat.id, 'Укажите ваш пол', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'sign_up' and
                                                 ProcessData.get_current_state(message.from_user.id) == 4)
def get_sex(message):
    if message.message:
        if message.data == "male" or message.data == "female":
            sex = message.data
            ProcessData.update_sex_user(message.from_user.id, sex)
            bot.send_message(message.message.chat.id, 'Спасибо за регистрацию {}!'.format(message.from_user.first_name))
            ProcessData.set_current_comm(message.from_user.id, '')
            ProcessData.set_current_state(message.from_user.id, 0)


@bot.message_handler(commands=['help'])
def send_help_info(message):
    """
        Вкладка помощи
    :param message:
    """
    bot.send_message(message.chat.id, 'Список возможных комманд и их описание')
    bot.send_message(message.chat.id, '/sign_up - регистрация\n'
                                      '/symptoms - перечислите свои симптомы и получите информацию о вашем возможном '
                                      'заболевании или укажите чем вы боле(ете\ли)\n'
                                      '/update_disease - обновите информацию о ваших прошлых заболеваниях\n')


@bot.message_handler(commands=['symptoms'])
def request_symptoms(message):
    """
        Получение симптомов пользователя, анализ, предсказание и выдача результата предсказания
    :param message:
    """
    ProcessData.set_current_comm(message.from_user.id, 'symptoms')
    ProcessData.set_current_state(message.from_user.id, 1)
    bot.send_message(message.chat.id, 'Укажите список ваших симтомов через запятую')


@bot.message_handler(func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'symptoms' and
                                          ProcessData.get_current_state(message.from_user.id) == 1)
def get_symptoms(message):
    ProcessData.set_symptoms(message.from_user.id, ProcessData.get_symptoms(message.from_user.id) + message.text + ', ')
    ProcessData.set_current_state(message.from_user.id, 2)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Я знаю чем я болею", callback_data='disease'))
    keyboard.add(InlineKeyboardButton("Мне нужен совет", callback_data='advice'))
    keyboard.add(InlineKeyboardButton("Я хочу добавить симптомы", callback_data='symptoms'))
    bot.send_message(message.chat.id, 'Вы хотите получить совет или вы знаете чем болеете?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'symptoms' and
                                                 ProcessData.get_current_state(message.from_user.id) == 2)
def get_disease_or_give_advice(message):
    if message.message:
        if message.data == "disease":
            bot.send_message(message.message.chat.id, "Дайте нам знать о вашей болезни")
            ProcessData.set_current_state(message.from_user.id, 3)
        elif message.data == "advice":
            bot.send_message(message.message.chat.id, "Это может занять некоторое время")
            predict_disease = NaiveBayesClassifiers().predict(ProcessData.get_clear_symptoms(message.from_user.id))
            ProcessData().put_predict_symptoms_to_db(ProcessData.get_symptoms(message.from_user.id),
                                                     message.from_user.id,
                                                     predict_disease)
            bot.send_message(message.message.chat.id, "Ваше возможно заболевание - {}".format(
                predict_disease.capitalize()))
            clear_states(message)
        elif message.data == "symptoms":
            bot.send_message(message.message.chat.id, 'Дополните список ваших симтомов через запятую')
            ProcessData.set_current_state(message.from_user.id, 1)


@bot.message_handler(func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'symptoms' and
                                          ProcessData.get_current_state(message.from_user.id) == 3)
def get_disease(message):
    ProcessData.set_disease(message.from_user.id, message.text)
    ProcessData().put_symptoms_to_db(ProcessData.get_symptoms(message.from_user.id),
                                     message.from_user.id,
                                     ProcessData.get_disease(message.from_user.id))
    bot.send_message(message.chat.id, 'Спасибо за информацию')
    clear_states(message)


@bot.message_handler(commands=['update_disease'])
def update_disease_get_list_of_symptoms_by_comm(message):
    """
        Обновление информации касательно болезней
    :param message:
    """
    update_disease_get_list_of_symptoms(message.chat.id, message.from_user.id)


def update_disease_get_list_of_symptoms(chat_id, user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("Обновить", callback_data='update'))
    keyboard.add(InlineKeyboardButton("Оценить", callback_data='assessment'))
    bot.send_message(chat_id, 'Вы хотите обновить информацию о болезни или оценить предсказание болезни?',
                     reply_markup=keyboard)

    ProcessData.set_current_state(user_id, 1)
    ProcessData.set_current_comm(user_id, 'update_or_assessment')


@bot.callback_query_handler(
    func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'update_or_assessment' and
                         ProcessData.get_current_state(message.from_user.id) == 1)
def update_disease_callback_inline(message):
    if message.message:
        if message.data == 'update':
            symptoms_without_disease = ProcessData().get_data_with_predict_disease(message.from_user.id)
            ProcessData.set_amount_of_block(message.from_user.id, len(symptoms_without_disease))
            if ProcessData.get_amount_of_block(message.from_user.id) != 0:
                bot.send_message(message.message.chat.id,
                                 'Укажите номер блока, по которому вы хотите обновить информацию о болезни\n'
                                 'Либо 0 если хотите прекратить выполнение операции\n'
                                 'В блоках указаны списки симптомов и соответсвующие им болезни, которые были предсказаны')
                for count, symptom in enumerate(symptoms_without_disease):
                    ProcessData.set_number_of_row(message.from_user.id,
                                                  ProcessData.get_number_of_row(message.from_user.id) +
                                                  str(symptom[0]) + SEPARATE_SYMBOL)
                    bot.send_message(message.message.chat.id, '№{}\n{}\nБолезнь: {}'.format(
                        count + 1,
                        ', '.join(symptom[1].split(';'))[:-2].capitalize(),
                        symptom[3].capitalize()))

                ProcessData.set_current_state(message.from_user.id, 1)
                ProcessData.set_current_comm(message.from_user.id, 'update_disease')
            elif ProcessData.get_amount_of_block(message.from_user.id) == 0:
                bot.send_message(message.message.chat.id, 'Нет данных для обновления')
                ProcessData.set_current_state(message.from_user.id, 0)
                ProcessData.set_current_comm(message.from_user.id, '')
        elif message.data == 'assessment':
            symptoms_without_disease = ProcessData().get_data_with_predict_disease(message.from_user.id)
            ProcessData.set_amount_of_block(message.from_user.id, len(symptoms_without_disease))
            if ProcessData.get_amount_of_block(message.from_user.id) != 0:
                bot.send_message(message.message.chat.id,
                                 'Укажите номер блока, в котором указано корректное заболевание\n'
                                 'Либо 0 если хотите прекратить выполнение операции\n'
                                 'В блоках указаны списки симптомов и соответсвующие им болезни, которые были предсказаны')
                for count, symptom in enumerate(symptoms_without_disease):
                    ProcessData.set_number_of_row(message.from_user.id,
                                                  ProcessData.get_number_of_row(message.from_user.id) +
                                                  str(symptom[0]) + SEPARATE_SYMBOL)
                    bot.send_message(message.message.chat.id, '№{}\n{}\nБолезнь: {}'.format(
                        count + 1,
                        ', '.join(symptom[1].split(';'))[:-2].capitalize(),
                        symptom[3].capitalize()))
                ProcessData.set_current_state(message.from_user.id, 1)
                ProcessData.set_current_comm(message.from_user.id, 'assessment')
            elif ProcessData.get_amount_of_block(message.from_user.id) == 0:
                bot.send_message(message.message.chat.id, 'Нет данных для оценки')
                ProcessData.set_current_state(message.from_user.id, 0)
                ProcessData.set_current_comm(message.from_user.id, '')


@bot.message_handler(func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'update_disease' and
                                          ProcessData.get_current_state(message.from_user.id) == 1)
def update_disease_get_number(message):
    if message.text.isdigit():
        if int(message.text) != 0:
            ProcessData.set_number_of_block(message.from_user.id, int(message.text))
            if ProcessData.get_number_of_block(message.from_user.id) <= ProcessData.get_amount_of_block(
                    message.from_user.id):
                ProcessData.set_current_state(message.from_user.id, 2)
                bot.send_message(message.chat.id, 'Укажите название болезни, которая соответствует этим симптомам')
            else:
                bot.send_message(message.chat.id, 'Пожалуйста введите номер от 1 до {}'.format(
                    ProcessData.get_amount_of_block(message.from_user.id)))
        else:
            ProcessData.set_number_of_block(message.from_user.id, 0)
            ProcessData.set_current_state(message.from_user.id, 0)
            ProcessData.set_current_comm(message.from_user.id, '')
            ProcessData.set_amount_of_block(message.from_user.id, 0)
            ProcessData.set_number_of_row(message.from_user.id, '')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста введите номер блока в числовом формате')


@bot.message_handler(func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'update_disease' and
                                          ProcessData.get_current_state(message.from_user.id) == 2)
def update_disease_get_number(message):
    ProcessData.set_disease(message.from_user.id, message.text)
    ProcessData().update_disease(ProcessData.get_disease(message.from_user.id),
                                 ProcessData.get_number_of_row(message.from_user.id),
                                 ProcessData.get_number_of_block(message.from_user.id))
    ProcessData.set_disease(message.from_user.id, '')
    ProcessData.set_symptoms(message.from_user.id, '')
    ProcessData.set_number_of_block(message.from_user.id, 0)
    ProcessData.set_number_of_row(message.from_user.id, '')
    if ProcessData.get_amount_of_block(message.from_user.id) == 1:
        clear_states(message)
        bot.send_message(message.chat.id, 'Спасибо за информацию')
    elif ProcessData.get_amount_of_block(message.from_user.id) > 1:
        ProcessData.set_current_state(message.from_user.id, 3)
        ProcessData.set_amount_of_block(message.from_user.id, 0)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(InlineKeyboardButton("Да", callback_data='yes'))
        keyboard.add(InlineKeyboardButton("Нет", callback_data='no'))
        bot.send_message(message.chat.id, 'Вы хотите указать болезни по другим блокам?',
                         reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'update_disease' and
                         ProcessData.get_current_state(message.from_user.id) == 3)
def callback_inline(message):
    if message.message:
        if message.data == "yes":
            ProcessData.set_current_state(message.from_user.id, 0)
            update_disease_get_list_of_symptoms(message.message.chat.id, message.from_user.id)
        elif message.data == "no":
            clear_states(message)
            bot.send_message(message.message.chat.id, 'Спасибо за информацию')


@bot.message_handler(func=lambda message: ProcessData.get_current_comm(message.from_user.id) == 'assessment' and
                                          ProcessData.get_current_state(message.from_user.id) == 1)
def update_disease_get_number(message):
    """
        Оценка правильности предсказаний
    :param message:
    """
    if message.text.isdigit():
        if int(message.text) != 0:
            ProcessData.set_number_of_block(message.from_user.id, int(message.text))
            if ProcessData.get_number_of_block(message.from_user.id) <= ProcessData.get_amount_of_block(
                    message.from_user.id):
                ProcessData().update_assessment(
                    ProcessData.get_number_of_block(message.from_user.id),
                    ProcessData.get_number_of_row(message.from_user.id))
                clear_states(message)
                bot.send_message(message.chat.id, 'Спасибо за информацию')
            else:
                bot.send_message(message.chat.id, 'Пожалуйста введите номер от 1 до {}'.format(
                    ProcessData.get_amount_of_block(message.from_user.id)))
        else:
            clear_states(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста введите номер блока в числовом формате')


def clear_states(message):
    ProcessData.set_current_state(message.from_user.id, 0)
    ProcessData.set_current_comm(message.from_user.id, '')
    ProcessData.set_symptoms(message.from_user.id, '')
    ProcessData.set_disease(message.from_user.id, '')
    ProcessData.set_number_of_block(message.from_user.id, 0)
    ProcessData.set_number_of_row(message.from_user.id, '')
    ProcessData.set_amount_of_block(message.from_user.id, 0)


bot.infinity_polling()
