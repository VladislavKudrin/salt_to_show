from django.db import models
from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse
import json
from django.contrib.auth import get_user_model




from .models import User_telegram, LoginMode, PayMode, TelegramActivation
from products.models import Product, ProductImage
from addresses.models import Address
from django.template.loader import get_template

BOT_TOKEN = getattr(settings, "BOT_TOKEN", '')

import telebot
from telebot import types

bot = telebot.TeleBot(BOT_TOKEN)
bot.set_webhook(url=settings.BASE_URL + "/api/telegram/")
User = get_user_model()

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
	markup = types.InlineKeyboardMarkup()
	user = User_telegram.objects.filter(chat_id=message.chat.id)
	bot.delete_message(message.chat.id, message.message_id)

	msg_welcome = "Чтобы начать оформление заказа, для начала нужно привязать бота к твоему аккаунту. Это займет меньше 2 минут. Для начала выбери ..."
	btn_login = types.InlineKeyboardButton(text='Login', callback_data='login')
	btn_register = types.InlineKeyboardButton(text='Register', url=settings.BASE_URL+reverse('login'))
	btn_logout = types.InlineKeyboardButton(text='Logout', callback_data='logout')

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
						context = {
							'user_address_name':user_address.name,
							'user_address_post_office':user_address.post_office,
							'user_address_phone':user_address.phone,
						}
						address_text = get_template("emails/telegram_address_confirm.html").render(context)
						btn1 = types.InlineKeyboardButton(text='Yes', callback_data='address_yes')
						btn2 = types.InlineKeyboardButton(text='No', callback_data='address_no')
						markup.row(btn1, btn2)
						bot.send_message(message.chat.id, address_text, parse_mode='HTML', reply_markup=markup)
				#pay mode
			else:
				markup.row(btn_logout)
				bot.send_message(message.chat.id, 'ToDO Menu', reply_markup=markup)
		else:
			markup.row(btn_login, btn_register)
			bot.send_message(message.chat.id, msg_welcome, parse_mode='HTML', reply_markup=markup)	
	else:
		markup.row(btn_login)
		bot.send_message(message.chat.id, msg_welcome, reply_markup=markup)
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
			#, reply_markup=types.ReplyKeyboardRemove() 
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
								provider_token='632593626:TEST:i53138327527',
								currency='UAH',
								prices=prices,
								start_parameter=product.slug,
								photo_url=product_img,
								photo_height=512,  
							    photo_width=512,
							    photo_size=512,
							    is_flexible=True				  
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
##THIS AFTER SENDS KEY##
@bot.message_handler(func=lambda c: c.text.split('_')[0] == '/mykey', content_types=['text'])
def authenticate_with_key(message):
	user_telegram = User_telegram.objects.filter(chat_id=message.chat.id)
	if user_telegram.exists():##check if exists
		user_telegram = user_telegram.first()
		if not user_telegram.is_logged_in:##check if logged in
			arr_key = message.text.split('_')
			if len(arr_key) == 2:##check if key 
				key = message.text.split('_')[1]
				activation = TelegramActivation.objects.filter(key=key, activated=False)
				if activation.exists():##check if key exists
					activation = activation.first()
					if user_telegram.chat_id == activation.chat_id: ##check if its his/her key
						user_salt = User.objects.filter(email=activation.email)
						if user_salt.exists():## check if salt user exists
							user_salt = user_salt.first()
							if user_salt.get_telegram() is None:##check if telegram is not binded with salt user
								user_telegram.user = user_salt
								activation.activated = True
								activation.save()
								user_telegram.save()
								markup = types.InlineKeyboardMarkup()
								btn1 = types.InlineKeyboardButton(text='Logout', callback_data='logout')
								markup.row(btn1)
								bot.send_message(message.chat.id, 'Success! Hello, '+user_salt.username, reply_markup=markup)
							else:
								markup = types.InlineKeyboardMarkup()
								btn1 = types.InlineKeyboardButton(text='Contact us', url=settings.BASE_URL + reverse('contact'))
								bot.send_message(message.chat.id, 'Hey, this account is already binded with "SALT Bot". If you cant unbind it or it wasnt you who did bind it, please, contact us!', reply_markup=markup)
					else:
						markup = types.InlineKeyboardMarkup()
						btn1 = types.InlineKeyboardButton(text='Login', callback_data='login')
						markup.row(btn1)
						bot.send_message(message.chat.id, 'This key is not from your account. Please send another one or login', reply_markup=markup)
				else:
					markup = types.InlineKeyboardMarkup()
					btn1 = types.InlineKeyboardButton(text='Login', callback_data='login')
					markup.row(btn1)
					bot.send_message(message.chat.id, 'There is no key like this or already activated, please Login to authenticate', reply_markup=markup)
		else:
			markup = types.InlineKeyboardMarkup()
			btn1 = types.InlineKeyboardButton(text='Logout', callback_data='logout')
			markup.row(btn1)
			bot.send_message(message.chat.id, 'You are already logged in', reply_markup=markup)
##THIS AFTER SENDS KEY##		

@bot.message_handler(func=check_login_mode, content_types=['text'])
def login_authentication(message):
	login_account_text = 'Go to your SALT account and enter key in form /mykey_(yourKey), where (yourKey) is key. You have '+ str(settings.TELEGRAM_ACTIVATION_EXPIRED) +' Minutes to do this. After that, you should send new activation!'
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
				user_salt = User.objects.filter(email=login_mode.email)
				if user_salt.exists():##if salt user exists
					activations = TelegramActivation.objects.filter(email=login_mode.email)
					if activations.exists():##if activation exists
						activation = activations.first()
						if activation.is_activated:#if activation activated, tell that its already activated, contact us
							bot.delete_message(message.chat.id, str(int(message.message_id)-1))
							markup = types.InlineKeyboardMarkup()
							btn1 = types.InlineKeyboardButton(text='Contact', url=settings.BASE_URL+reverse('contact'))
							markup.row(btn1)
							bot.send_message(message.chat.id, 'This Email is already successfully activated. If it wasnt you, contact us!', reply_markup=markup)
							user_telegram.exit_all_modes()
						else:#if not activated activation exists
							if activation.can_activate():#if not activated activation exists and can be activated, send that can confirm it. This should prevent spams
								markup_account = types.InlineKeyboardMarkup()
								btn_account = types.InlineKeyboardButton(text='Go to SALT account', url=settings.BASE_URL+reverse('accounts:user-update'))
								markup_account.row(btn_account)
								bot.delete_message(message.chat.id, str(int(message.message_id)-1))
								bot.send_message(message.chat.id, 'Go to your SALT account and enter key in form /mykey_(yourKey), where (yourKey) is key.', reply_markup=markup_account)
								user_telegram.exit_all_modes()
							else:#if not activated activation exists and can't be activated, delete old activation and send new one OR TELL HIM THAT OLD ONE EXPIRED AND ASK IF HE WANTS TO SEND NEW ONE
								markup_account = types.InlineKeyboardMarkup()
								btn_account = types.InlineKeyboardButton(text='Go to SALT account', url=settings.BASE_URL+reverse('accounts:user-update'))
								markup_account.row(btn_account)
								activations.delete()
								TelegramActivation.objects.create(chat_id=message.chat.id, email=login_mode.email)
								bot.send_message(message.chat.id, login_account_text, reply_markup=markup_account)
								user_telegram.exit_all_modes()

					else:##if no activation exists, create new activation
						markup_account = types.InlineKeyboardMarkup()
						btn_account = types.InlineKeyboardButton(text='Go to SALT account', url=settings.BASE_URL+reverse('accounts:user-update'))
						markup_account.row(btn_account)
						TelegramActivation.objects.create(chat_id=message.chat.id, email=login_mode.email)
						bot.delete_message(message.chat.id, str(int(message.message_id)-1))
						bot.send_message(message.chat.id, login_account_text, reply_markup=markup_account)
						user_telegram.exit_all_modes()
				else:##if no salt user under this email
					bot.delete_message(message.chat.id, str(int(message.message_id)-1))
					markup = types.InlineKeyboardMarkup()
					btn1 = types.InlineKeyboardButton(text='Register', url=settings.BASE_URL+reverse('login'))
					btn2 = types.InlineKeyboardButton(text='Login', callback_data='login')
					markup.row(btn1, btn2)
					bot.send_message(message.chat.id, 'There is no user with this email, would you like to register? Or try again.', reply_markup=markup)
					user_telegram.exit_all_modes()
###############LOGIN EMAIL PASSWORD AUTH###############



###############SIMPLE MESSAGE HANDLER###############
@bot.message_handler(content_types=['text'])
def send_message(message):				
	bot.send_message(message.chat.id, "Didn't understand u!")
###############SIMPLE MESSAGE HANDLER###############







#############PRODUCT FUNCTION#############
def send_message_to_channel(product):
	# users = User_telegram.objects.all()
	images = ProductImage.objects.filter(product=product).order_by('image_order')
	context = {
			'product_url':settings.BASE_URL+product.get_absolute_url(),
			'product_price':str(product.price_original),
			'product_currency':product.currency_original,
			'product_title':product.title,
			'product_condition':product.condition.condition_ru,
			'product_description':product.description,
			'product_shipping_price':product.national_shipping,
			'start_purchase_url': "https://t.me/saltish_bot?start="+product.slug,
	}
	text = get_template("emails/telegram_new_item.html").render(context)
	media_types = []
	if images.exists():
		for image in images:
			if image.image_order == 1:
				media_type=types.InputMediaPhoto(media=image.image, caption=text, parse_mode='HTML')
				media_types.append(media_type)
			else:
				media_type=types.InputMediaPhoto(media=image.image)
				media_types.append(media_type)
		bot.send_media_group('@saltish_channel', media=media_types, timeout=1000)
#############PRODUCT FUNCTION#############


#############PRODUCT SOLD NOTIFICATION#############
def send_message_to_seller(chat_id):
	markup = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton(text='Go to your orders', url=settings.BASE_URL+reverse('orders:list')+'?tab=sold')
	markup.row(btn1)
	bot.send_message(chat_id, 'Hi! You have just sold an item!', reply_markup=markup)

#############PRODUCT SOLD NOTIFICATION#############










		

	
