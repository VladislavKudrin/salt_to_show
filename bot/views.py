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



@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
	print(pre_checkout_query)
	bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types='successful_payment')
def process_successful_payment(message: types.Message):
	print(message)



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
"""
						markup = types.InlineKeyboardMarkup()
						btn1 = types.InlineKeyboardButton(text='Yes', callback_data='address_yes')
						btn2 = types.InlineKeyboardButton(text='No', callback_data='address_no')
						markup.row(btn1, btn2)
						bot.send_message(message.chat.id, 
								address_text,
								parse_mode='HTML', reply_markup=markup)
					#pay mode
			else:
				markup = types.InlineKeyboardMarkup()
				btn1 = types.InlineKeyboardButton(text='Logout', callback_data='logout')
				markup.row(btn1)
				bot.send_message(message.chat.id, 'ToDO Menu', reply_markup=markup)
		else:
			markup = types.InlineKeyboardMarkup()
			btn1 = types.InlineKeyboardButton(text='Login', callback_data='login')
			markup.row(btn1)
			bot.send_message(message.chat.id, 'Please use "Login" to authenticate!', reply_markup=markup)	
	else:
		markup = types.InlineKeyboardMarkup()
		btn1 = types.InlineKeyboardButton(text='Login', callback_data='login')
		markup.row(btn1)
		bot.send_message(message.chat.id, 'Welcome to SALT bot, please use "Login" to authenticate!', reply_markup=markup)
		user, created = User_telegram.objects.get_or_create(chat_id = message.chat.id)

###############LOGIN###############
@bot.callback_query_handler(func=lambda c: c.data == 'login')
def process_callback_login(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
	user_telegram = User_telegram.objects.filter(chat_id=callback_query.from_user.id)
	if user_telegram.exists():
		user_telegram = user_telegram.first()
		if user_telegram.is_logged_in:
			user_telegram.exit_all_modes()
			markup = types.InlineKeyboardMarkup()
			btn1 = types.InlineKeyboardButton(text='Logout', callback_data='logout')
			markup.row(btn1)
			bot.send_message(callback_query.from_user.id, 'You are already logged in! Please use "Logout" for setting new account.', reply_markup=markup)
		else:
			#begin login
			user_telegram.exit_all_modes()
			user_telegram.in_answer_mode=True
			user_telegram.save()
			bot.send_message(callback_query.from_user.id, 'Please, enter your email')
			LoginMode.objects.get_or_create(user_telegram=user_telegram)
			#begin login
	else:
		bot.send_message(message.chat.id, 'Hello, first time around? Please use /start to tune our bot.')
###############LOGIN################


###############LOGOUT###############
@bot.callback_query_handler(func=lambda c: c.data == 'logout')
def process_callback_logout(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
	user_telegram = User_telegram.objects.filter(chat_id=callback_query.from_user.id)
	if user_telegram.exists():
		user_telegram = user_telegram.first()
		user_telegram.exit_all_modes()
		user_telegram.user=None
		user_telegram.save()
		markup = types.InlineKeyboardMarkup()
		btn1 = types.InlineKeyboardButton(text='Login', callback_data='login')
		markup.row(btn1)
		bot.send_message(callback_query.from_user.id, 'Successfully logged out. Please, use "Login" to log in.', reply_markup=markup)
	else:
		bot.send_message(callback_query.from_user.id, 'Hello, first time around? Please use /start to tune our bot.')
###############LOGOUT###############


###############PAY ADDRESS CONFIRMATION###############
@bot.callback_query_handler(func=lambda c: c.data == 'address_yes' or c.data == 'address_no')
def process_callback_address_confirmation(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
	user_telegram = User_telegram.objects.filter(chat_id=callback_query.from_user.id)
	if user_telegram.exists():
		user_telegram = user_telegram.first()
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
						if callback_query.data == 'address_yes':
							user_telegram.exit_all_modes()
							bot.send_invoice(callback_query.from_user.id, 
								title=product.title, 
								description = product.description, 
								invoice_payload=product.slug, 
								provider_token='635983722:TEST:i53138327527',
								currency='UAH',
								prices=prices,
								start_parameter=product.slug,
								photo_url=product_img,
								photo_height=512,  
							    photo_width=512,
							    photo_size=512				  
								)
						elif callback_query.data == 'address_no':
							user_telegram.exit_all_modes()
							markup = types.InlineKeyboardMarkup()
							btn1 = types.InlineKeyboardButton(text='Change Address', url=settings.BASE_URL+reverse('accounts:user-update'))
							btn2 = types.InlineKeyboardButton(text='BUY Again', url='https://t.me/saltish_bot?start='+product.slug)
							markup.row(btn1, btn2)
							bot.send_message(callback_query.from_user.id, 
									'Choose:',
									reply_markup=markup)
					else:
						user_telegram.exit_all_modes()
						bot.send_message(callback_query.from_user.id, 'You cant buy this item.')
				else:
					bot.send_message(callback_query.from_user.id, 'There is no such item')
###############PAY ADDRESS CONFIRMATION###############		



###############LOGIN EMAIL PASSWORD AUTH###############
def check_login_mode(message):
	user_telegram = User_telegram.objects.filter(chat_id=message.chat.id)
	if user_telegram.exists():
		user_telegram=user_telegram.first()
		return user_telegram.get_mode() == 'login'

@bot.message_handler(func=check_login_mode, content_types=['text'])
def login_authentication(message):
	user_telegram = User_telegram.objects.filter(chat_id=message.chat.id)
	if user_telegram.exists():
		user_telegram=user_telegram.first()
		login_mode = LoginMode.objects.filter(user_telegram=user_telegram)
		if login_mode.exists():
			login_mode = login_mode.first()
			if not login_mode.email and not login_mode.password:
				login_mode.email = message.text.lower()
				login_mode.save()
				bot.delete_message(message.chat.id, message.message_id)#delete 'Email'
				bot.send_message(message.chat.id, 'Please, enter your password')
			elif login_mode.email and not login_mode.password:
				login_mode.password = message.text
				login_mode.save()
				user = authenticate(username=login_mode.email, password=login_mode.password)
				if user is None:
					user_telegram.exit_all_modes()
					bot.delete_message(message.chat.id, message.message_id)#delete 'Password'
					bot.delete_message(message.chat.id, str(int(message.message_id)-3))#delete 'Enter Email'
					bot.delete_message(message.chat.id, str(int(message.message_id)-1))#delete 'Enter Password'
					markup = types.InlineKeyboardMarkup()
					btn1 = types.InlineKeyboardButton(text='Login', callback_data='login')
					markup.row(btn1)
					bot.send_message(message.chat.id, 'The password seems to be wrong. "Login" to try again.', reply_markup=markup)
				else:
					if user.get_telegram() is None:
						user_telegram.user = user
						user_telegram.save()
						bot.delete_message(message.chat.id, message.message_id)#delete 'Password'
						bot.delete_message(message.chat.id, str(int(message.message_id)-3))#delete 'Enter Email'
						bot.delete_message(message.chat.id, str(int(message.message_id)-1))#delete 'Enter Password'
						markup = types.InlineKeyboardMarkup()
						btn1 = types.InlineKeyboardButton(text='Logout', callback_data='logout')
						markup.row(btn1)
						bot.send_message(message.chat.id, 'Success! Hello, ' + user.username + '.', reply_markup=markup)
						user_telegram.exit_all_modes()
					else:
						markup = types.InlineKeyboardMarkup()
						btn1 = types.InlineKeyboardButton(text='Contact us', url=settings.BASE_URL + reverse('contact'))
						markup.row(btn1)
						bot.send_message(message.chat.id, 'Hey, this account is already binded with "SALT Bot". If you cant unbind it or it wasnt you who did bind it, please, contact us!', reply_markup=markup)
						user_telegram.exit_all_modes()
###############LOGIN EMAIL PASSWORD AUTH###############



###############SIMPLE MESSAGE HANDLER###############
@bot.message_handler(content_types=['text'])
def send_message(message):				
	bot.send_message(message.chat.id, message.text)
###############SIMPLE MESSAGE HANDLER###############







#############PRODUCT FUNCTION#############
def send_message_to_channel(product):
	# users = User_telegram.objects.all()
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
		bot.send_media_group('@saltish_channel', media=media_types)
#############PRODUCT FUNCTION#############


#############PRODUCT SOLD NOTIFICATION#############
def send_message_to_seller(chat_id):
	markup = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton(text='Go to your orders', url=settings.BASE_URL+reverse('orders:list')+'?tab=sold')
	markup.row(btn1)
	bot.send_message(chat_id, 'Hi! You have just sold an item!', reply_markup=markup)

#############PRODUCT SOLD NOTIFICATION#############










		

	
