import math
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.conf import settings

from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart
from ecommerce.utils import unique_order_id_generator
from chat_ecommerce.models import Thread
from products.models import Product
from liqpay.liqpay3 import LiqPay
LIQPAY_PRIV_KEY = getattr(settings, "LIQPAY_PRIVATE_KEY", "sandbox_tLSKnsdkFbQgIe8eiK8Y2RcaQ3XUJl29quSa4aSG")
LIQPAY_PUB_KEY =  getattr(settings, "LIQPAY_PUBLIC_KEY", 'sandbox_i6955995458')
import requests
import json


ORDER_STATUS_CHOICES = (
	('created', 'Created'),
	('hold_wait', 'Paid'),
	('shipped', 'Shipped'),
	('refunded', 'Refunded'),
	)

class OrderManagerQuerySet(models.query.QuerySet):
	def by_request(self, request):
		billing_profile, created = BillingProfile.objects.new_or_get(request)
		return self.filter(billing_profile=billing_profile)
	def not_created(self):
		return self.exclude(status='created')
class OrderManager(models.Manager):
	def get_queryset(self):
		return OrderManagerQuerySet(self.model, using=self.db)
	def new_or_get(self, billing_profile, product):
		created=False
		qs = self.get_queryset().filter(
			billing_profile=billing_profile, 
			product=product, 
			active=True,
			status='created'
			)
		if qs.count()==1:
			obj=qs.first()

		else:
			obj=self.model.objects.create(
				billing_profile=billing_profile, 
				product=product)
			created = True		
		return obj, created

	def by_request(self, request):
		return self.get_queryset().by_request(request)


class Order(models.Model):
	order_id               = models.CharField(max_length=120, blank = True)
	billing_profile        = models.ForeignKey(BillingProfile, null=True, blank=True)
	shipping_address       = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True)
	billing_address        = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True)
	shipping_address_final = models.TextField(blank=True, null=True)
	billing_address_final  = models.TextField(blank=True, null=True)
	# cart                 = models.ForeignKey(Cart)
	product                = models.OneToOneField(Product, blank=True, null=True)
	status                 = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
	shipping_total         = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
	total                  = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	active                 = models.BooleanField(default=True)
	objects                = OrderManager()
	timestamp              = models.DateTimeField(auto_now_add=True)
	updated                = models.DateTimeField(auto_now=True)
	thread                 = models.OneToOneField(Thread, null=True, blank=True)

	def __str__(self):
		return self.order_id

	class Meta:
		ordering = ['-timestamp', '-updated']
	def convert_total(self, user):
		total = self.total
		region_user = user.region
		if region_user:
			convertet_total = round((int(total)/region_user.currency_mult),6)
		return convertet_total
	def get_status(self):
		return self.get_status_display()


	def get_absolute_url(self):
		return reverse("orders:detail", kwargs={'order_id':self.order_id})

	def update_total(self):
		product_total = 0
		shipping_total = 0
		if self.product.price:
			product_total = self.product.price
		if self.product.shipping_price:
			shipping_total=self.product.shipping_price.national_shipping
		new_total = math.fsum([product_total, shipping_total])
		formatted_total = format(new_total, '.2f')
		self.total=formatted_total
		self.save()
		return new_total

	def check_done(self):
		billing_profile = self.billing_profile
		shipping_address = self.shipping_address
		billing_address = self.billing_address
		total = self.total
		if billing_profile and shipping_address and billing_address and total > 0:
			return True
		return False

	def mark_paid(self):
		if self.check_done():
			self.status = "paid"
			self.save()
		return self.status

	def complete_this_order(self, request):
		liqpay = LiqPay(LIQPAY_PUB_KEY, LIQPAY_PRIV_KEY)
		params = {
			"action"        : "hold_completion",
			"version"       : "3",
			"order_id"      : self.order_id
		}
		signature = liqpay.cnb_signature(params)
		data = liqpay.cnb_data(params)
		payload_with_token = {
   			"data": data,
   			"signature":signature
				}
		response = requests.post('https://www.liqpay.ua/api/request', data=payload_with_token)
		response_json = response.json()
		if response_json.get('status') == 'success':
			self.transaction.complete_transaction(response.json())
			self.status = 'shipped'
			self.save()
			if self.product:
				self.product.active = False
				self.product.save()
		else:
			self.transaction.transaction_error(response.json())


def pre_save_create_order_id(sender, instance, *args, **kwargs):
	if not instance.order_id:
		instance.order_id=unique_order_id_generator(instance)
	qs=Order.objects.filter(product=instance.product).exclude(billing_profile=instance.billing_profile)
	if qs.exists():
		qs.update(active=False)

	if instance.shipping_address and not instance.shipping_address_final:
	    instance.shipping_address_final = instance.shipping_address.get_address()

	if instance.billing_address and not instance.billing_address_final:
	    instance.billing_address_final = instance.billing_address.get_address()
	"""
Допустим, пользовател зашел как гость, создается корзина, привязанная к сессии,
после ввода имейла создается профиль оплаты. Профиль оплаты и корзина проверяется
на существование заказа с такой же привязкой к корзине и профилю (ничего не найдет, 
если до этого не заходил на чекаут, если зашел, погулял по сайту и зашел обратно, то
заказ останется тот же), если ничего не найдено, то создается новый заказ,
который привязывается к корзине и профилю. Если гость захотел залогиниться и 
продолжить - после логина произойдет проверка на checkout.view (поиск уже существующего
заказа, ничего не найдет, так как сессия, а соответсвенно корзина, осталась та же
, но профиль обновился, так как был привязан к зарегистрированному пользователю), 
после проверки создается новый заказ, с залогиненным профилем и старой корзиной, так
как сессия не поменялась. Сессия(корзина) менятеся(удаляется) после логаута. 
Так как создается новый заказ, то происходит сигнал pre_save, который создает
уникальный стринг заказа, а так же фильтрует все заказы на наличие действующей корзины.
Находит две корзины, старого профиля(гостя) и пользователя. Исключает нового 
пользователя, остается старый заказ, который был создат с профиля гостя.
Делает заказ неактивным

	"""
pre_save.connect(pre_save_create_order_id, sender=Order)


# def post_save_cart_total(sender, instance, created, *args, **kwargs):
# #метод, если заказ обновляется вместе с корзиной
# 	if not created:
# 		cart_obj=instance
# 		cart_total=cart_obj.total
# 		cart_id=cart_obj.id
# 		qs=Order.objects.filter(cart__id=cart_id)
# 		if qs.count()==1:
# 			order_obj = qs.first()
# 			order_obj.update_total()


# post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
#метод, если заказ создан сразу, новый и без добавления - оплачивать
	if created:
		instance.update_total()

post_save.connect(post_save_order, sender=Order)

class TransactionManager(models.Manager):
	def new_or_get(self, order, data):
		qs = self.get_queryset().filter(
			order = order
			)
		if qs.count()==1:
			obj=qs.first()
		else:
			obj=self.model.objects.create(
				order=order, 
				data_initiation=data)	
		return obj

class Transaction(models.Model):
	order             = models.OneToOneField(Order, null=True, blank=True)
	data_initiation   = models.TextField(null=True, blank=True)
	data_completition = models.TextField(null=True, blank=True)
	data_error        = models.TextField(null=True, blank=True)
	complete          = models.BooleanField(default=False)
	objects           = TransactionManager()

	def complete_transaction(self, data):
		if self.complete == False:
			self.data_completition = data
			self.complete = True
			self.save()

	def transaction_error(self, data):
		self.data_error = data
		self.save






















