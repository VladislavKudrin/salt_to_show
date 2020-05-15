from django.db import models
from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse
import json

from .models import User_telegram, LoginMode, PayMode
from products.models import Product, ProductImage
from addresses.models import Address

BOT_TOKEN = getattr(settings, "BOT_TOKEN", '')

import telebot
from telebot import types

bot = telebot.TeleBot(BOT_TOKEN)


class BotView(APIView):
	def post(self, request):
		json_string = request.body.decode("UTF-8")
		update = telebot.types.Update.de_json(json_string)
		bot.process_new_updates([update])
		return Response({"code":200})


@bot.message_handler(commands=['start'])
def start(message):
	user = User_telegram.objects.filter(chat_id=message.chat.id)
	bot.delete_message(message.chat.id, message.message_id)
	if user.exists():
		user = user.first()
		if user.is_logged_in == True:
			product_slug = (message.text).split('/start ')
			if len(product_slug) > 1:
				product_slug = product_slug[1]
				#pay mode
				user.exit_all_modes()
				user.in_answer_mode=True
				user.save()
				billing_profile = user.get_billing_profile()
				if billing_profile is not None:
					user_address = Address.objects.filter(billing_profile = billing_profile)
					if user_address.exists():
						user_address = user_address.first()
						PayMode.objects.get_or_create(user_telegram=user, product_slug=product_slug)
						address_text = """
Is it correct address to send the item? 
<b>Name:</b> <i>"""+user_address.name+"""</i>
<b>Post office:</b> <i>"""+user_address.post_office+"""</i>
<b>Phone:</b> <i>"""+user_address.phone+"""</i>
/yes or /no
"""
						bot.send_message(message.chat.id, 
								address_text,
								parse_mode='HTML')
					#pay mode
		else:
			bot.send_message(message.chat.id, 'Please use /login to authenticate!')	
	else:
		bot.send_message(message.chat.id, 'Welcome to SALT bot, please use /login to authenticate!')
		user, created = User_telegram.objects.get_or_create(chat_id = message.chat.id)


@bot.message_handler(commands=['login'])
def login(message):
	user_telegram = User_telegram.objects.filter(chat_id=message.chat.id)
	if user_telegram.exists():
		user_telegram = user_telegram.first()
		if user_telegram.is_logged_in:
			user_telegram.exit_all_modes()
			bot.send_message(message.chat.id, 'You are already logged in! Please use /logout for setting new account.')
		else:
			#begin login
			user_telegram.exit_all_modes()
			user_telegram.in_answer_mode=True
			user_telegram.save()
			bot.send_message(message.chat.id, 'Please, enter your email')
			LoginMode.objects.get_or_create(user_telegram=user_telegram)
			#begin login
	else:
		bot.send_message(message.chat.id, 'Hello, first time around? Please use /start to tune our bot.')

@bot.message_handler(commands=['logout'])
def logout(message):
	user_telegram = User_telegram.objects.filter(chat_id=message.chat.id)
	if user_telegram.exists():
		user_telegram = user_telegram.first()
		user_telegram.exit_all_modes()
		user_telegram.user=None
		user_telegram.save()
		bot.send_message(message.chat.id, 'Successfully logged out. Please, use /login to log in.')
	else:
		bot.send_message(message.chat.id, 'Hello, first time around? Please use /start to tune our bot.')

# @bot.callback_query_handler(func=lambda c: c.data == 'login')
# def process_callback_login(callback_query: types.CallbackQuery):
# 	bot.answer_callback_query(callback_query.id)
# 	bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
# 	user_telegram = User_telegram.objects.filter(chat_id=callback_query.from_user.id)
# 	if user_telegram.exists():
# 		user_telegram = user_telegram.first()
# 		if user_telegram.is_logged_in:
# 			user_telegram.exit_all_modes()
# 			markup = types.InlineKeyboardMarkup()
# 			btn1 = types.InlineKeyboardButton(text='Logout', callback_data='logout')
# 			markup.row(btn1)
# 			bot.send_message(callback_query.from_user.id, 'You are already logged in! Please use "Logout" for setting new account.', reply_markup=markup)
# 		else:
# 			#begin login
# 			user_telegram.exit_all_modes()
# 			user_telegram.in_answer_mode=True
# 			user_telegram.save()
# 			bot.send_message(callback_query.from_user.id, 'Please, enter your email')
# 			LoginMode.objects.get_or_create(user_telegram=user_telegram)
# 			#begin login
# 	else:
# 		bot.send_message(message.chat.id, 'Hello, first time around? Please use /start to tune our bot.')

# @bot.message_handler(commands=['test'])
# def test(message):
# 	markup = types.InlineKeyboardMarkup()
# 	btn1 = types.InlineKeyboardButton(text='Login', callback_data='login')
# 	markup.row(btn1)
# 	bot.send_message(message.chat.id,'Welcome to SALT bot, please use "Login" to authenticate!', reply_markup=markup)



@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
	print(pre_checkout_query)
	bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types='successful_payment')
def process_successful_payment(message: types.Message):
	print(message)



def send_message_to_channel(product):
	users = User_telegram.objects.all()
	images = ProductImage.objects.filter(product=product).order_by('image_order')
	media_types = []
	if images.exists():
		for image in images:
			if image.image_order == 1:
				text = """🧂<b>Title:</b> <i>"""+product.title+"""</i>
🧂<b>Description:</b> <i>"""+product.description+"""</i>
""""""🧂<b>Price:</b> <i>"""+str(product.price_original)+' '+product.currency_original+"""</i>
""""""<b>.</b>
""""""<b>.</b>
""""""<b><ins><a href="https://t.me/saltish_bot?start="""+product.slug+"""">BUY</a></ins></b>"""
				media_type=types.InputMediaPhoto(media=image.image, caption=text, parse_mode='HTML')
				media_types.append(media_type)
			else:
				media_type=types.InputMediaPhoto(media=image.image)
				media_types.append(media_type)
		# markup = types.InlineKeyboardMarkup()
		# button = types.InlineKeyboardButton(text='Go to Checkout', url='https://t.me/saltish_bot?start='+product.slug)
		# markup.row(button)
		bot.send_media_group('@saltish_channel', media=media_types)
		# bot.send_message('@saltish_channel', reply_markup=markup, text = 'BUY')



@bot.message_handler(content_types=['text'])
def modes_interaction(message):
	user_telegram = User_telegram.objects.filter(chat_id=message.chat.id)
	if user_telegram.exists():
		user_telegram=user_telegram.first()
		# if login
		if user_telegram.get_mode() == 'login':
			login_mode = LoginMode.objects.filter(user_telegram=user_telegram)
			if login_mode.exists():
				login_mode = login_mode.first()
				if not login_mode.email and not login_mode.password:
					login_mode.email = message.text
					login_mode.save()
					bot.delete_message(message.chat.id, message.message_id)
					bot.send_message(message.chat.id, 'Please, enter your password')
				elif login_mode.email and not login_mode.password:
					login_mode.password = message.text
					login_mode.save()
					user = authenticate(username=login_mode.email, password=login_mode.password)
					if user is None:
						user_telegram.exit_all_modes()
						bot.delete_message(message.chat.id, message.message_id)
						bot.send_message(message.chat.id, 'The password seems to be wrong. Type /login to try again.')
					else:
						user_telegram.user = user
						user_telegram.save()
						bot.delete_message(message.chat.id, message.message_id)
						bot.send_message(message.chat.id, 'Success! Hello, ' + user.username + '.')
						user_telegram.exit_all_modes()
		#if login
		#if pay
		if user_telegram.get_mode() == 'pay':
			pay_mode = PayMode.objects.filter(user_telegram=user_telegram)
			if pay_mode.exists():
				pay_mode = pay_mode.first()
				product = Product.objects.filter(slug=pay_mode.product_slug)
				if product.exists():
					product = product.first()
					if not product.is_paid and product.is_payable and product.is_active and product.is_authentic:
						product_img = product.thumbnail.first().get_absolute_url()
						prices = [types.LabeledPrice('Price', int(product.price_original)*100),types.LabeledPrice('Shipping', int(product.national_shipping)*100)]
						if message.text == '/yes':
							user_telegram.exit_all_modes()
							bot.send_invoice(message.chat.id, 
								title=product.title, 
								description = product.description, 
								invoice_payload=product.slug, 
								provider_token='635983722:LIVE:i53138327527',
								currency='UAH',
								prices=prices,
								start_parameter=product.slug,
								photo_url=product_img,
								photo_height=512,  
							    photo_width=512,
							    photo_size=512				  
								)
						elif message.text == '/no':
							user_telegram.exit_all_modes()
							bot.send_message(message.chat.id, 
									'Please, go to <b><a href="'+settings.BASE_URL+reverse('accounts:user-update')+'">Change Address</a></b> and try to <b><ins><a href="https://t.me/saltish_bot?start='+product.slug+'">BUY</a></ins></b> again.',
									parse_mode='HTML')
					else:
						user_telegram.exit_all_modes()
						bot.send_message(message.chat.id, 'You cant buy this item.')
				else:
					bot.send_message(message.chat.id, 'There is no such item')
		#if pay
		else:
			bot.send_message(message.chat.id, message.text)

				






@bot.message_handler(content_types=['text'])
def send_message(message):
	bot.send_poll(message.chat.id, question='How are you today?', options=['a','b','c'])



# @bot.message_handler(commands=['product'])
# def send_message(message):
# 	product_slug = (message.text).split('/product ')
# 	print(message)
# # 	if len(product_slug) > 1:
# # 		product_slug = product_slug[1]
# # 		product = Product.objects.filter(slug=product_slug)
# # 		if product.exists():
# # 			product = product.first()
# # 			images = ProductImage.objects.filter(product=product).order_by('image_order')
# # 			images_dict = {}
# # 			media_types = []
# # 			if images.exists():
# # 				for image in images:
# # 					if image.image_order == 1:
# # 						text = """🧂<b>Title:</b> <i>"""+product.title+"""</i>
# # 🧂<b>Description:</b> <i>"""+product.description+"""</i>
# # """"""🧂<b>Price:</b> <i>"""+str(product.price)+"""</i>
# # """
# # 						media_type=types.InputMediaPhoto(media=image.image, caption=text, parse_mode='HTML')
# # 						media_types.append(media_type)
# # 					else:
# # 						media_type=types.InputMediaPhoto(media=image.image)
# # 						media_types.append(media_type)
# # 			bot.send_media_group(message.chat.id, media=media_types)
# # 		else:
# # 			bot.send_message(message.chat.id, 'There is no such item')
# # 	else:
# # 		bot.send_message(message.chat.id, 'Please enter product slug')
		

	
