import re
import telebot
from constants import API_KEY
import random
import datetime
import requests

bot = telebot.TeleBot(API_KEY, parse_mode=None)


# Bot lintenning type only text
@bot.message_handler(content_types=['text'])
def echo_all(message):
    if message.text == 'hi':
        bot.reply_to(message, 'hello')
    elif message.text == 'hello':
        bot.reply_to(message, 'hey')
    elif message.text == 'last':
        # last character.
        bot.reply_to(message, message.text[-1])
    elif message.text == 'first':
        # first character.
        bot.reply_to(message, message.text[0])
    elif message.text == 'upper':
        # upper character.
        bot.reply_to(message, message.text.upper())
    elif message.text == 'reverse':
        # reverse the string
        bot.reply_to(message, message.text[::-1])
    elif message.text == 'password':
        # Auto Generate password for user length 6
        gener_password(message)
        # user_input = int(message.text)
        # for i in range(user_input):
        #         random_num = random.randint(user_input, 999999)
        #         bot.reply_to(message, random_num)
    elif message.text == 'info':
        # invoke funtion
        user_info(message)
    elif message.text == 'mygrade':
        get_score(message)
    elif message.text == 'date':
        current_date(message)
    elif message.text == 'user':
        dict_users(message)
    elif message.text == 'number':
        input_number(message)
    elif message.text == 'html code':
        get_html(message)
    elif message.text == 'check':
        check_input(message)
    else:
        bot.reply_to(message, "Sorry i don't understand")


def user_info(message):
    sent_msg = bot.send_message(message.chat.id, "what's your name?")
    bot.register_next_step_handler(sent_msg, name_handler)  # Next message will call the name_handler function


def name_handler(message):
    name = message.text
    sent_msg = bot.send_message(message.chat.id, f"Your name is {name}. how old are you?")
    bot.register_next_step_handler(sent_msg, age_handler, name)  # Next message will call the age_handler function


def age_handler(message, name):
    age = message.text
    bot.send_message(message.chat.id, f"Your name is {name}, and your age is {age}.")


def get_score(message):
    sent_msg = bot.send_message(message.chat.id, "Enter your score here ")
    bot.register_next_step_handler(sent_msg, get_grade)  # Next message will call the get_grade function


def get_grade(message):
    try:
        grade = int(message.text)
        if grade >= 90 and grade <= 100:
            bot.send_message(message.chat.id, f"Your grade is {grade} so you get A")
        elif grade >= 80 and grade < 90:
            bot.send_message(message.chat.id, f"Your grade is {grade} so you get B")
        elif grade >= 70 and grade < 80:
            bot.send_message(message.chat.id, f"Your grade is {grade} so you get C")
        elif grade >= 60 and grade < 70:
            bot.send_message(message.chat.id, f"Your grade is {grade} so you get D")
        elif grade >= 0 and grade < 60:
            bot.send_message(message.chat.id, f"Your grade is {grade} so you get E")
        elif grade < 0:
            bot.send_message(message.chat.id, f"Your grade is {grade} so you get F")
    except:
        middler_ware(message)


def current_date(message):
    d = datetime.datetime.today()
    todate = d.strftime('%Y/%m/%d')
    bot.send_message(message.chat.id, todate)

# takes 1 string list as a parameter that contains usernames and return a dictionary array with two keys:
# "username"  and  "ID" . For each username add a new element (dictionary) with incremental ID
def dict_users(message):
    data = message.text
    id = 1
    newdict = []
    for item in data:
        newdict.append({'username': item, 'ID': id})
        id += 1
    # Print on terminal
    print(newdict)
    bot.send_message(message.chat.id, newdict)


def input_number(message):
    sent_msg = bot.send_message(message.chat.id, "Enter the number here ... ")
    bot.register_next_step_handler(sent_msg, check_number)  # Next message will call the get_grade function


# to check if input as the number divide by 2 equal 0 is even
def check_number(message):
    try:
        number = int(message.text)
        if number % 2 == 0:
            bot.send_message(message.chat.id, 'This is EVEN number')
        else:
            bot.send_message(message.chat.id, 'This is ODD number')
    except:
        middler_ware(message)


def gener_password(message):
    sent_msg = bot.send_message(message.chat.id, "Enter your auto generate")
    bot.register_next_step_handler(sent_msg, auto_gener)


# random number which has 6 digits and allow user to input how many random they want to see as the output
def auto_gener(message):
    try:
        user_input = int(message.text)
        for i in range(user_input):
            random_num = random.randint(user_input, 999999)
            bot.reply_to(message, random_num)
    except:
        middler_ware(message)


# to handler any error if user input wrong
def middler_ware(message):
    bot.send_message(message.chat.id, "PLease follow the instruction :) ")


# takes one string in argument that represents a valid url
def get_html(message):
    sent_msg = bot.send_message(message.chat.id, "Enter any valid url")
    bot.register_next_step_handler(sent_msg, return_html)


# RETURN the HTML Code of the page as string
def return_html(message):
    try:
        link = message.text
        res = requests.get(link)
        print(res.text)
    except:
        middler_ware(message)


def check_input(message):
    sent_msg = bot.send_message(message.chat.id, "Detects string contain only in [a-k / A-K and 0-5]")
    bot.register_next_step_handler(sent_msg, check_rule)


def check_rule(message):
    txt = message.text
    if len(txt) == 0:
        return middler_ware(message)
    else:
        data = re.sub('[a-kA-K0-5]', '', txt)
        if len(data) == 0:
            bot.send_message(message.chat.id, "True")
        else:
            return middler_ware(message)
# PollBot is an automated account that runs through a script built by a third-party Telegram developer. The bot helps Telegram users to create poll questions and conduct polls.
bot.polling()
