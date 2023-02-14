import requests
import telebot
import json

from config import currencies, TOKEN
from extentions import CryptoConverter, UserException


curr_bot = telebot.TeleBot(TOKEN)


#  handler for /start command
@curr_bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    text = "Hi there! This Bot will help you with currency conversion" \
           "\n\nTo start calculation enter this command: /try" \
           "\n(Or use this command to check all commands available to use with Bot: /help )"
    curr_bot.reply_to(message, text)


#  handler for /help command
#  shows the whole list of commands available in Bot
@curr_bot.message_handler(commands=["help"])
def start(message: telebot.types.Message):
    text = "The whole list of commands available in Bot:" \
           "\n\n - /start - to start Bot" \
           "\n - /try - to enter values for conversion" \
           "\n - /values - to check currencies available for conversion" \
           "\n - /help - to check all commands available to use with Bot" \
           "\n - /info - to get information about Bot"
    curr_bot.reply_to(message, text)


#  handler for /try command
#  asks for values from user to execute conversion
@curr_bot.message_handler(commands=["try"])
def get_input(message: telebot.types.Message):
    text = "Enter this info to do calculations (with the spaces in between):\n" \
    "\n- what currency you would like to purchause (title in English)" \
    "\n- what currency you will pay in" \
    "\n- what amount you need (periods allowed)" \
    "\n\n(To see all currencies available to use in Bot run this command: /values)"
    curr_bot.reply_to(message, text)


#  handler for /values command
#  shows all currencies available to use in bot
@curr_bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "List of currencies available to use in converter:\n"
    for currency in currencies.keys():
        text = text + f"\n- {currency}"
        #  text = "\n-".join(text, currency)
    curr_bot.reply_to(message, text)


# handler to provide brief info about Bot
@curr_bot.message_handler(commands=["info"])
def info(message: telebot.types.Message):
    text = "Currency exchange rates are sourced from cryptocompare.com through open API" \
           "\n\nApp is created by Ksenia El., 2023"
    curr_bot.reply_to(message, text)


#  handler to process user input of values to execute conversion
@curr_bot.message_handler(content_types=["text"])
def get_result(message: telebot.types.Message):
    try:
        message_lower_case = message.text.lower()
        user_input = message_lower_case.split(" ")
        # list of 3 values: currency to buy, currency to pay, amount of purchase
        # (created from user input)
        if len(user_input) != 3:  # in case user entered less or more than 3 required values
            raise UserException("Three values are required.\n\nUse this command to try again: /try")
        #  in case everything is okay with user input
        exch_currency, base_currency, amount = user_input
        exchange_rate = CryptoConverter.get_exchange_rate(exch_currency, base_currency, amount)

    except UserException as exception_type_one:
        curr_bot.reply_to(message, f"Can't process your request (invalid user input). {exception_type_one}")

    except Exception as exception_type_two:
        curr_bot.reply_to(message, f"Can't process your request (error of the system). Try later with this command: /try \n{exception_type_two}")

    #  in case everything is okay with user input - it provides result of calculations
    else:
        result = round((exchange_rate * float(amount)), 2) # calculate the result plus round it to 2 decimal points
        text = f"Total price of {amount} {exch_currency}(s) in {base_currency}(s) is: {result}"
        # it sends a message with the result of exchange calculations to
        # the chat with the user who made a request (user is identified by id)
        curr_bot.send_message(message.chat.id, text)


# handler to reply for any invalid content type of user input
@curr_bot.message_handler(content_types=["audio", "photo", "voice", "voice", "document", "location", "contact", "sticker"])
def other_content(message: telebot.types.Message):
    text = "Invalid type of input (only text format accepted)\n\nUse this command to try again: /try"
    curr_bot.reply_to(message, text)


#  to run Bot nonstop
curr_bot.polling(none_stop=True)  # it makes the bot working all the time




