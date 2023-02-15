# CurrencyConverterBot

Simple Telegram-bot to execute currency conversion (calculates total price for purchasing some amount of some currency).

This Bot knows the following commands:

/start command - to reply with the welcoming message and info about the main commands to use
/try command - to ask for 3 values required and execute currency conversion
/values command - to provide info about all curencies available to use with Bot
/help command - to return all commands available in Bot
/info command - to show all main info about Bot

Has separate handlers for user and system errors. 

Supports conversion of 6 different kinds of currency. Exchange rates are sourced from cryptocompare.com through open API.

