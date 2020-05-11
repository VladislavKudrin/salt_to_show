from django.db import models
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User_telegram

BOT_TOKEN = getattr(settings, "BOT_TOKEN", '')

import telebot

bot = telebot.TeleBot(BOT_TOKEN)


class BotView(APIView):
	def post(self, request):
		json_string = request.body.decode("UTF-8")
		update = telebot.types.Update.de_json(json_string)
		bot.process_new_updates([update])

		return Response({"code":200})


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, 'Hi')
	user = User_telegram()
	user.user_id = message.chat.id
	user.save()


@bot.message_handler(commands=['text'])
def send_message(message):
	bot.send_message(message.chat.id, 'hi again')