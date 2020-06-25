from django.db import models
from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse
import json
from django.contrib.auth import get_user_model
from django.template.loader import get_template
import telebot
from telebot import types
from ecommerce.utils import stay_where_you_are
from .models import User_telegram, LoginMode, PayMode, TelegramActivation, ChannelProductMessage
from products.models import Product, ProductImage
from addresses.models import Address
import copy

base_url = settings.BASE_URL
BOT_TOKEN = getattr(settings, "BOT_TOKEN", '')
bot = telebot.TeleBot(BOT_TOKEN)
# if not settings.TESTSERVER and not settings.LIVE:
# 	bot.set_webhook(url=base_url + "/api/telegram/")
User = get_user_model()
telegra_activation_exp = str(settings.TELEGRAM_ACTIVATION_EXPIRED)


# Messages
msg_welcome = "Чтобы начать оформление заказа, нужно привязать бота к твоему аккаунту. Это займет меньше 2 минут.\n\nДля начала выбери:"
already_logged_in_msg = "Ты уже залогинен_а. Нажми на кнопку Логаут, чтобы настроить новый аккаунт."
enter_email_msg = "Пожалуйста, введи свой мэйл."
start_msg = 'Привет, ты тут впервые?👋 Нажми на "Начать", чтобы настроить нашего бота.'
logout_msg = "Пока!🖐 Чтобы снова войти, нажми на кнопку Логин."
cant_buy_msg = "К сожалению, кто-то оказался быстрее 😟 Вещь продана!"
no_item_msg = "Ой, а такой вещи не существует 🧐"
wrong_address_msg = "Ничего страшного! Вот что нужно сделать, чтобы оформить заказ на другой адрес:"
already_binded_msg = "Этот аккаунт уже привязан к SALT Bot.\n\nЕсли ты этого не делал_а или не можешь переключиться на другой аккаунт, свяжись с нами! 📝"
wrong_key_msg = "Этот ключ не принадлежит твоему акканту. Пожалуйста, введи верный ключ.\n\nЕсли у тебя не получается это сделать, напиши нам! 📝"
no_key_msg = "Такого ключа не существует или он уже был использован ранее. Пожалуйста, залогинься еще раз, чтобы получить новый ключ."
already_logged_in_msg = "Ты уже залогинен_а."
enter_key_msg = """
Чтобы привязать свой SALT аккаунт к этому боту, перейди в настройки аккаунта, скопируй ключ и вставь его сюда.\n\n
У тебя есть целых """ + telegra_activation_exp + """ минут (после этого придется повторить логин)."""
enter_key_msg_2 = """
Чтобы привязать свой SALT аккаунт к этому боту, перейди в настройки аккаунта, скопируй ключ и вставь его сюда.\n\n 
Если что-то не получается, попробуй удалить ключ и залогиниться заново."""
no_user_msg = """
Пользователя с таким мэйлом не существует.\n\nМожет ты просто допустил_а ошибку? Нажми на Логин и попробуй ввести свой мэйл еще раз.\n\nИли ты хочешь зарегистрироваться? Тогда жми на кнопку Регистрация."""
email_activated = "Этот мэйл уже успешно активирован. Если ты этого не делал_а, свяжись с нами! 📝"
sold_msg_channel = 'Продано 💥'
buyer_bought_msg = 'Это было быстро, да? 🚀 Оплата твоего заказа прошла успешно. Мы проинформировали продавца отправить тебе купленную вещь в течение 24 часов.'

# Urls 
support_url = 'https://t.me/salt_roman'
channel_url = 'https://t.me/saltish_channel'
channel = '@saltish_channel'
bot_start_url = 'https://t.me/saltish_bot?start='
register = base_url+'/login'
get_code = base_url+'/account/telegram-activation'
go_to_orders_sold = base_url+'/orders/?tab=sold'
go_to_orders_buy = base_url+'/orders/?tab=buy'
change_address_url = base_url+'/account/details'

# Buttons
btn_login = types.InlineKeyboardButton(text='Логин', callback_data='login')
btn_register = types.InlineKeyboardButton(text='Регистрация', url=register)
btn_logout = types.InlineKeyboardButton(text='Логаут', callback_data='logout')
btn_contact = types.InlineKeyboardButton(text='Проблема?', url=support_url)
btn_go_to_channel = types.InlineKeyboardButton(text='Выбрать другие айтемы на канале', url=channel_url, callback_data='logout')
btn_address_yes = types.InlineKeyboardButton(text='Да', callback_data='address_yes')
btn_address_no = types.InlineKeyboardButton(text='Нет', callback_data='address_no')
btn_get_key = types.InlineKeyboardButton(text='Перейти на SALT', url=get_code)
btn_go_to_orders_sold = types.InlineKeyboardButton(text='Перейти к заказам', url=go_to_orders_sold)
btn_go_to_orders_buy = types.InlineKeyboardButton(text='Перейти к заказам', url=go_to_orders_buy)

# Base markup
markup = types.InlineKeyboardMarkup()

# Markup leading to purchase
markup_1 = copy.deepcopy(markup)
markup_1.row(btn_go_to_channel)
markup_1.row(btn_logout, btn_contact)

# Markup address confirmation
markup_2 = copy.deepcopy(markup)
markup_2.row(btn_address_yes, btn_address_no)

# Markup with logout button
markup_3 = copy.deepcopy(markup)
markup_3.row(btn_logout)

# Markup with login and register buttons
markup_4 = copy.deepcopy(markup)
markup_4.row(btn_login, btn_register)

# Markup with login button
markup_5 = copy.deepcopy(markup)
markup_5.row(btn_login)

# Markup with contact button
markup_6 = copy.deepcopy(markup)
markup_6.row(btn_contact)

# Markup with contact and login button
markup_7 = copy.deepcopy(markup)
markup_7.row(btn_logout, btn_contact)

# Markup to get the key from account
markup_8 = copy.deepcopy(markup)
markup_8.row(btn_get_key)

# Markup with go to orders button
markup_9 = copy.deepcopy(markup)
markup_9.row(btn_go_to_orders_sold)

# Markup for start
markup_10 = copy.deepcopy(markup)
markup_10.row(btn_go_to_channel)
markup_10.row(btn_login, btn_logout)
markup_10.row(btn_contact)

# Markup with go to orders button
markup_11 = copy.deepcopy(markup)
markup_11.row(btn_go_to_orders_buy)


class BotView(APIView):
	def post(self, request):
		json_string = request.body.decode("UTF-8")
		update = telebot.types.Update.de_json(json_string)
		bot.process_new_updates([update])
		return Response({"code":200})

def delete_activation_key_view(request):
	user = request.user
	if user.is_authenticated():
		activations = TelegramActivation.objects.filter(email=user.email)
		if activations.exists():
			activations.delete()
	return stay_where_you_are(request)

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
	chat_id = pre_checkout_query.from_user.id
	product_slug = pre_checkout_query.invoice_payload
	product = Product.objects.filter(slug = product_slug, active=True)
	if product.exists():
		product = product.first()
		if not product.is_paid and product.is_payable and product.is_active and product.is_authentic:
			user_telegram = User_telegram.objects.filter(chat_id=chat_id)
			if user_telegram.exists():
				user_telegram = user_telegram.first()
				billing_profile = user_telegram.get_billing_profile()
				if billing_profile:
					user_address = billing_profile.get_address()
					if user_address:
						from orders.models import Order
						order, created = Order.objects.new_or_get(billing_profile, product)
						order.shipping_address = user_address
						order.save()
						bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
					else:
						bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False)
				else:
					bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False)
			else:
				bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False)
		else:
			bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False)
	else:
		bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False)

@bot.message_handler(content_types='successful_payment')
def process_successful_payment(message: types.Message):
	slug = message.successful_payment.invoice_payload
	chat_id = message.from_user.id
	product = Product.objects.filter(slug=slug)
	if product.exists():
		product = product.first()
		user_telegram = User_telegram.objects.filter(chat_id=chat_id)
		if user_telegram.exists():
			user_telegram = user_telegram.first()
			billing_profile = user_telegram.get_billing_profile()
			if billing_profile:
				from orders.models import Order
				order = Order.objects.filter(
						billing_profile=billing_profile, 
						product=product, 
						active=True,
						status='created'
						)
				if order.exists():
					order = order.first()
					from orders.models import Transaction
					transaction = Transaction.objects.new_or_get(order=order, data=message)	
					order.status = "paid"
					order.save()
					channel_message = ChannelProductMessage.objects.filter(product_slug=slug)
					if channel_message.exists():
						channel_message = channel_message.first()
						bot.edit_message_caption(sold_msg_channel, channel_message.chat_id, channel_message.message_id)
					if order.product:
						bot.send_message(chat_id, buyer_bought_msg, reply_markup=markup_11)
						order.send_email(success=True)	




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
						context = {
							'user_address_name':user_address.name,
							'user_address_post_office':user_address.post_office,
							'user_address_phone':user_address.phone,
						}
						address_text = get_template("bot/emails/telegram_address_confirm.html").render(context)
						bot.send_message(message.chat.id, address_text, parse_mode='HTML', reply_markup=markup_2)
				#pay mode
			else:
				context = {
					'products': Product.objects.recent_10(),
				}
				reply = get_template("bot/emails/telegram_start_menu.html").render(context)
				bot.send_message(message.chat.id, reply, reply_markup=markup_10, parse_mode='HTML')
		else:
			bot.send_message(message.chat.id, msg_welcome, parse_mode='HTML', reply_markup=markup_4)	
	else:
		bot.send_message(message.chat.id, msg_welcome, reply_markup=markup_4)
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
			bot.send_message(callback_query.from_user.id, already_logged_in_msg, reply_markup=markup_3)
		else:
			#begin login
			user_telegram.exit_all_modes()
			user_telegram.in_answer_mode=True
			user_telegram.save()
			bot.send_message(callback_query.from_user.id, enter_email_msg)
			LoginMode.objects.get_or_create(user_telegram=user_telegram)
			#begin login
	else:
		bot.send_message(message.chat.id, start_msg)
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
		bot.send_message(callback_query.from_user.id, logout_msg, reply_markup=markup_5)
	else:
		bot.send_message(callback_query.from_user.id, start_msg)
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
								provider_token='635983722:LIVE:i53138327527',
								currency='UAH',
								prices=prices,
								start_parameter=product.slug,
								photo_url=product_img,
								photo_height=512,  
							    photo_width=512,
							    photo_size=512,
							    is_flexible=False				  
								)
						elif callback_query.data == 'address_no':
							user_telegram.exit_all_modes()
							markup_change_address = types.InlineKeyboardMarkup()
							btn1 = types.InlineKeyboardButton(text='1. Изменить адрес', url=change_address_url)
							btn2 = types.InlineKeyboardButton(text='2. Нажать сюда, затем на "Начать" ⬇️', url=bot_start_url+product.slug)
							markup_change_address.row(btn1)
							markup_change_address.row(btn2)
							bot.send_message(callback_query.from_user.id, wrong_address_msg, reply_markup=markup_change_address)
					else:
						user_telegram.exit_all_modes()
						bot.send_message(callback_query.from_user.id, cant_buy_msg)
				else:
					bot.send_message(callback_query.from_user.id, no_item_msg)
###############PAY ADDRESS CONFIRMATION###############		


###############LOGIN EMAIL PASSWORD AUTH###############
def check_login_mode(message):
	user_telegram = User_telegram.objects.filter(chat_id=message.chat.id)
	if user_telegram.exists():
		user_telegram=user_telegram.first()
		return user_telegram.get_mode() == 'login'


##THIS AFTER SENDS KEY##
@bot.message_handler(func=lambda c: c.text is not None and '/mykey' in c.text, content_types=['text'])
def authenticate_with_key(message):
	user_telegram = User_telegram.objects.filter(chat_id=message.chat.id)
	if user_telegram.exists():##check if exists
		user_telegram = user_telegram.first()
		if not user_telegram.is_logged_in:##check if logged in
			key = message.text # be careful here
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
							context = {
								'products': Product.objects.recent_10(),
								'username': user_salt.username
							}
							reply = get_template("bot/emails/telegram_recent_10.html").render(context)
							bot.send_message(message.chat.id, reply, reply_markup=markup_1, parse_mode='HTML')

						else:
							bot.send_message(message.chat.id, already_binded_msg, reply_markup=markup_6)
				else:
					bot.send_message(message.chat.id, wrong_key, reply_markup=markup_7)
			else:
				bot.send_message(message.chat.id, no_key_msg, reply_markup=markup_5)
		else:
			bot.send_message(message.chat.id, already_logged_in_msg, reply_markup=markup_3)

##THIS AFTER SENDS KEY##		

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
				user_salt = User.objects.filter(email=login_mode.email)
				if user_salt.exists():##if salt user exists
					if user_salt.first().get_telegram() is None:
						activations = TelegramActivation.objects.filter(email=login_mode.email)
						if activations.exists():##if activation exists
							activation = activations.first()
							if activation.is_activated:#if activation activated, tell that its already activated, contact us
								bot.delete_message(message.chat.id, str(int(message.message_id)-1))
								bot.send_message(message.chat.id, email_activated, reply_markup=markup_6)
								user_telegram.exit_all_modes()
							else:#if not activated activation exists
								if activation.can_activate():#if not activated activation exists and can be activated, send that can confirm it. This should prevent spams
									bot.delete_message(message.chat.id, str(int(message.message_id)-1))
									bot.send_message(message.chat.id, enter_key_msg_2, reply_markup=markup_8)
									user_telegram.exit_all_modes()
								else:#if not activated activation exists and can't be activated, delete old activation and send new one OR TELL HIM THAT OLD ONE EXPIRED AND ASK IF HE WANTS TO SEND NEW ONE
									activations.delete()
									TelegramActivation.objects.create(chat_id=message.chat.id, email=login_mode.email)
									bot.send_message(message.chat.id, enter_key_msg, reply_markup=markup_8)
									user_telegram.exit_all_modes()
						else:##if no activation exists, create new activation
							TelegramActivation.objects.create(chat_id=message.chat.id, email=login_mode.email)
							bot.delete_message(message.chat.id, str(int(message.message_id)-1))
							bot.send_message(message.chat.id, enter_key_msg, reply_markup=markup_8)
							user_telegram.exit_all_modes()
					else:
						bot.send_message(message.chat.id, already_binded_msg, reply_markup=markup_6)
				else:##if no salt user under this email
					bot.delete_message(message.chat.id, str(int(message.message_id)-1))
					bot.send_message(message.chat.id, no_user_msg, reply_markup=markup_4)
					user_telegram.exit_all_modes()
###############LOGIN EMAIL PASSWORD AUTH###############


###############SIMPLE MESSAGE HANDLER###############
@bot.message_handler(content_types=['text'])
def send_message(message):	
	context = {
		'products': Product.objects.recent_10(),
	}
	reply = get_template("bot/emails/telegram_react_nonsense.html").render(context)
	bot.send_message(message.chat.id, reply, reply_markup=markup_10, parse_mode='HTML')
###############SIMPLE MESSAGE HANDLER###############




#############PRODUCT FUNCTION#############
def send_message_to_channel(product):
	# users = User_telegram.objects.all()
	images = ProductImage.objects.filter(product=product).order_by('image_order')
	context = {
			'product_url':base_url+product.get_absolute_url(),
			'product_price':str(product.price_original),
			'product_currency':product.currency_original,
			'product_title':product.title,
			'product_condition':product.condition.condition_ru,
			'product_description':product.description,
			'product_shipping_price':product.national_shipping,
			'start_purchase_url': bot_start_url+product.slug,
	}
	text = get_template("bot/emails/telegram_new_item.html").render(context)
	media_types = []
	if images.exists():
		for image in images:
			new_image = image.compress(size=(1000, 1000))
			if image.image_order == 1:
				media_type=types.InputMediaPhoto(media=new_image, caption=text, parse_mode='HTML')
				media_types.append(media_type)
			else:
				media_type=types.InputMediaPhoto(media=new_image)
				media_types.append(media_type)
		message = bot.send_media_group(channel, media=media_types, timeout=1000)
		ChannelProductMessage.objects.get_or_create(chat_id=channel, product_slug=product.slug, message_id=message[0].message_id)
		new_image.close()
#############PRODUCT FUNCTION#############


#############PRODUCT SOLD NOTIFICATION#############
def send_message_to_seller(chat_id, item=None):
	context = {
		'product_title':item.title,
	}
	message = get_template("bot/emails/telegram_item_sold.html").render(context)
	bot.send_message(chat_id, message, reply_markup=markup_9, parse_mode='HTML')

#############PRODUCT SOLD NOTIFICATION#############










		

	
