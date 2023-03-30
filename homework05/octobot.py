import telebot
import gspread
import json
import pandas as pd
import re
from datetime import datetime, timedelta

bot = telebot.TeleBot("6141360664:AAGVlc06n8U8g2-zx5JFTmXGpeonnOFdBpQ")
connected_sheet = False


def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    # PUT YOUR CODE HERE
    pass


def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    # PUT YOUR CODE HERE
    pass


def convert_date(date: str = "01/01/00"):
    """Конвертируем дату из строки в datetime"""
    # PUT YOUR CODE HERE
    pass


def connect_table(message):
    """Подключаемся к Google-таблице"""
    url = message.text
    sheet_id = '1jgK-YFPufB-hPWvcHAbiUumz5TVRhHX0qV13VhpJYaE'  # Нужно извлечь id страницы из ссылки на Google-таблицу
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open("tables.json", "w") as json_file:
        json.dump(tables, json_file)
    global connected_sheet
    connected_sheet = True
    bot.send_message(message.chat.id, "Таблица подключена!")


def connected_table():
    with open("tables.json") as json_file:
        return True if json_file.readline() != "" else False


def access_current_sheet(df=pd.DataFrame):
    """ Обращаемся к Google-таблице """
    with open("tables.json") as json_file:
        tables = json.load(json_file)
    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Преобразуем Google-таблицу вц таблицу pandas
    return worksheet, tables[max(tables)]["url"], df


def input_data():
    """ Вводим данные в Google-таблицу """
    worksheet, url, df = access_current_sheet()
    # Запрашиваем данные от пользователя
    subject = input("Введите предмет: ")
    link = input("Введите ссылку на предмет: ")
    date = input("Введите дату сдачи предмета: ")
    worksheet.append_row([subject, link, date])
    return "Данные успешно добавлены в таблицу"


def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        connect_table(message)

    elif message.text == "Редактировать предметы":
        subj_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        subj_markup.row("Добавить новый предмет")
        subj_markup.row("Удалить предмет")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=subj_markup)
        bot.register_next_step_handler(info, choose_subject_action)

    elif message.text == "Редактировать дедлайн":
        deadline_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        deadline_markup.row("Добавить новый дедлайн")
        deadline_markup.row("Удалить дедлайн")
        deadline_markup.row("Изменить дедлайн")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=deadline_markup)
        bot.register_next_step_handler(info, choose_deadline_action)

    elif message.text == "Посмотреть дедлайны на этой неделе":
        # PUT YOUR CODE HERE
        pass


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    if message.text == "Добавить новый предмет":
        subj = bot.send_message(message.chat.id, "Введите название предмета: ")
        bot.register_next_step_handler(subj, add_new_subject)

    elif message.text == "Удалить предмет":
        delete_subject(message)


def choose_deadline_action(message):
    """Выбираем действие в разделе Редактировать дедлайн"""
    # PUT YOUR CODE HERE
    pass


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    # PUT YOUR CODE HERE
    pass


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    # PUT YOUR CODE HERE
    pass


def update_subject_deadline(message):
    """Обновляем дедлайн"""
    # PUT YOUR CODE HERE
    pass


def add_new_subject(message):
    """Вносим новое название предмета в Google-таблицу"""
    subject = message.text

    link = bot.send_message(message.chat.id, "Введите ссылку на таблицу: ")
    bot.register_next_step_handler(link, add_new_subject_url, subject)


def add_new_subject_url(message, subject):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    link = message.text

    worksheet, url, df = access_current_sheet()
    worksheet.append_row([subject, link])

    print(df())


def update_subject(message):
    """Обновляем информацию о предмете в Google-таблице"""
    # PUT YOUR CODE HERE
    pass


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    # PUT YOUR CODE HERE
    bot.send_message(message.chat.id, "123123")


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=["start"])
def start(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if not connected_table():
        start_markup.row("Подключить Google-таблицу")
    start_markup.row("Посмотреть дедлайны на этой неделе")
    start_markup.row("Редактировать дедлайн")
    start_markup.row("Редактировать предметы")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


bot.infinity_polling()
