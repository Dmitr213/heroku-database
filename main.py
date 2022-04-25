import telebot
import os
import logging
from flask import Flask, request
from telebot import types
from bs4 import BeautifulSoup
from urllib.request import *
from config import *
import time


bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setlevel(logging.DEBUG)
project = 0


def keyboardDelite(message):
    bot.edit_message_text('message.text', message.chat.id, message.message_id, reply_markup=None)


@bot.message_handler(commands=['start'])
def start(message):
    global project
    project = 0

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Мои работы')
    button2 = types.KeyboardButton('Мой сайт')
    button3 = types.KeyboardButton('Заказать проект')
    button4 = types.KeyboardButton('Услуги')
    button5 = types.KeyboardButton('Кто я такая')
    markup.add(button1, button2, button3, button4, button5)

    mess = f'Приветулички-красатулички,  <b>{message.from_user.first_name} {message.from_user.last_name}' \
           f'</b>, на связи Карина'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Вау, крутое фото!')


@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    website = types.KeyboardButton('Вебсайт')
    start = types.KeyboardButton('Start')
    markup.add(website, start)
    bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    global project
    get_message_bot = message.text.strip().lower()

    if get_message_bot == "привет" or message.text == 'привет!' or message.text == 'ghbdtn':
        bot.send_message(message.chat.id, f"И тебе привет, {message.from_user.first_name}!", parse_mode='html')

    elif get_message_bot == "главное меню":
        project = 0

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Мои работы')
        button2 = types.KeyboardButton('Мой сайт')
        button3 = types.KeyboardButton('Заказать проект')
        button4 = types.KeyboardButton('Услуги')
        button5 = types.KeyboardButton('Кто я такая')
        markup.add(button1, button2, button3, button4, button5)

        mess = 'Выбери, что тебя интересует:'
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

    elif get_message_bot == "кто я такая":
        photo = open('my_photo.jpg', 'rb')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Главное меню')
        markup.add(button)
        mess = 'Я человек'
        bot.send_photo(message.chat.id, photo, mess, parse_mode='html', reply_markup=markup)


    elif get_message_bot == "мои работы" or (get_message_bot == "предыдущая работа" and project == 2):
        html = urlopen(Request('https://www.behance.net/rinchan3')).read()
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.select('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC'
                           ' > div > div > div > div > div > div.ContentGrid-grid-px7 > div:nth-child(1) > div >'
                           ' div > div.Cover-content-yv3 > img')
        url1 = soup.select('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC >'
                          ' div > div > div > div > div > div.ContentGrid-grid-px7 > div:nth-child(1) > div > div'
                          ' > div.Cover-overlay-r1A.Cover-showOnHover-oZ2 > a')[0]['href']

        image_url = temp[0]['src']
        name = temp[0]['alt']
        urlretrieve(image_url, '1.png')
        image = open('1.png', 'rb')

        markup = types.InlineKeyboardMarkup()
        inlbutton = types.InlineKeyboardButton("Посмотреть проект полностью", url=url1)
        markup.row(inlbutton)
        bot.send_photo(message.chat.id, image, name, reply_markup=markup)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton('Следующая работа')
        button2 = types.KeyboardButton('Главное меню')
        markup.add(button1, button2)
        bot.send_message(message.chat.id, 'Это мой последний проект', reply_markup=markup)

        project = 1

    elif (get_message_bot == "следующая работа" and project == 1) or (get_message_bot == "предыдущая работа" and project == 3):

        html = urlopen(Request('https://www.behance.net/rinchan3')).read()
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.select('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC >'
                           ' div > div > div > div > div > div.ContentGrid-grid-px7 > div:nth-child(2) > div > div'
                           ' > div.Cover-content-yv3 > img')
        url1 = soup.select('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC >'
                           ' div > div > div > div > div > div.ContentGrid-grid-px7 > div:nth-child(2) > div > div'
                           ' > div.Cover-overlay-r1A.Cover-showOnHover-oZ2 > a')[0]['href']

        image_url = temp[0]['src']
        name = temp[0]['alt']
        urlretrieve(image_url, '2.png')
        image = open('2.png', 'rb')

        markup = types.InlineKeyboardMarkup()
        inlbutton = types.InlineKeyboardButton("Посмотреть проект полностью", url=url1)
        markup.row(inlbutton)
        bot.send_photo(message.chat.id, image, name, reply_markup=markup)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton('Предыдущая работа')
        button2 = types.KeyboardButton('Следующая работа')
        button3 = types.KeyboardButton('Главное меню')
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, 'Это ещё один мой проект', reply_markup=markup)

        project = 2

    elif (get_message_bot == "следующая работа" and project == 2) or (get_message_bot == "предыдущая работа" and project == 4):

        html = urlopen(Request('https://www.behance.net/rinchan3')).read()
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.select('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC > div'
                           ' > div > div > div > div > div.ContentGrid-grid-px7 > div:nth-child(3) > div > div >'
                           ' div.Cover-content-yv3 > img')
        url1 = soup.select('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC >'
                           ' div > div > div > div > div > div.ContentGrid-grid-px7 > div:nth-child(3) > div > div'
                           ' > div.Cover-overlay-r1A.Cover-showOnHover-oZ2 > a')[0]['href']

        image_url = temp[0]['src']
        name = temp[0]['alt']
        urlretrieve(image_url, '3.png')
        image = open('3.png', 'rb')

        markup = types.InlineKeyboardMarkup()
        inlbutton = types.InlineKeyboardButton("Посмотреть проект полностью", url=url1)
        markup.row(inlbutton)
        bot.send_photo(message.chat.id, image, name, reply_markup=markup)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton('Предыдущая работа')
        button2 = types.KeyboardButton('Следующая работа')
        button3 = types.KeyboardButton('Главное меню')
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, 'Это ещё один мой проект', reply_markup=markup)

        project = 3

    elif (get_message_bot == "следующая работа" and project == 3) or (get_message_bot == "предыдущая работа" and project == 5):

        html = urlopen(Request('https://www.behance.net/rinchan3')).read()
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.select('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC > div'
                           ' > div > div > div > div > div.ContentGrid-grid-px7 > div:nth-child(4) > div > div >'
                           ' div.Cover-content-yv3 > img')
        url1 = soup.select('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC >'
                           ' div > div > div > div > div > div.ContentGrid-grid-px7 > div:nth-child(4) > div > div'
                           ' > div.Cover-overlay-r1A.Cover-showOnHover-oZ2 > a')[0]['href']

        image_url = temp[0]['src']
        name = temp[0]['alt']
        urlretrieve(image_url, '4.png')
        image = open('4.png', 'rb')

        markup = types.InlineKeyboardMarkup()
        inlbutton = types.InlineKeyboardButton("Посмотреть проект полностью", url=url1)
        markup.row(inlbutton)
        bot.send_photo(message.chat.id, image, name, reply_markup=markup)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton('Предыдущая работа')
        button2 = types.KeyboardButton('Следующая работа')
        button3 = types.KeyboardButton('Главное меню')
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, 'Это ещё один мой проект', reply_markup=markup)

        project = 4

    elif get_message_bot == "следующая работа" and project == 4:

        html = urlopen(Request('https://www.behance.net/rinchan3')).read()
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.select('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC > div'
                           ' > div > div > div > div > div.ContentGrid-grid-px7 > div:nth-child(5) > div > div >'
                           ' div.Cover-content-yv3 > img')
        url1 = soup.select('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC > div'
                           ' > div > div > div > div > div.ContentGrid-grid-px7 > div:nth-child(5) > div > div >'
                           ' div.Cover-overlay-r1A.Cover-showOnHover-oZ2 > a')[0]['href']

        image_url = temp[0]['src']
        name = temp[0]['alt']
        urlretrieve(image_url, '5.png')
        image = open('5.png', 'rb')

        markup = types.InlineKeyboardMarkup()
        inlbutton = types.InlineKeyboardButton("Посмотреть проект полностью", url=url1)
        markup.row(inlbutton)
        bot.send_photo(message.chat.id, image, name, reply_markup=markup)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton('Предыдущая работа')
        button2 = types.KeyboardButton('Главное меню')
        markup.add(button1, button2)
        bot.send_message(message.chat.id, 'Это ещё один мой проект', reply_markup=markup)

        project = 5

    elif get_message_bot == "photo":
        photo = open('popugai-agressivni.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
    elif get_message_bot == "location":
        bot.send_location(message.chat.id, 55.750300, 37.537239)
    else:
        bot.send_message(message.chat.id, "Эх... так я не пойму тебя, добрый человек. \n\nНажимай ка лучше на кнопки. "
                                          "Если их нет то напиши /help", parse_mode='html')

@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    bot.remove_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

bot.polling(none_stop=True)