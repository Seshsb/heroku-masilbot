import os
import telebot
import logging
import datetime
import re

from telebot import types
from flask import Flask, request
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


BOT_TOKEN = os.environ.get('BOT_TOKEN')
YANDEX_TOKEN = os.environ.get('YANDEX_TOKEN')
ADMIN = os.environ.get('ADMIN')

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)