import numpy
from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.translation import pgettext
from django.core.mail import send_mail
from django.utils.safestring import mark_safe

from ecommerce.utils import add_message, stay_where_you_are, custom_render
from ecommerce.mixins import RequestFormAttachMixin
from analitics.mixins import ObjectViewedMixin
from carts.models import Cart
from categories.models import Size, Brand, Undercategory, Overcategory, Gender, Category, Condition
from accounts.models import Wishlist
from .models import Product, ProductImage, ProductThumbnail, ReportedProduct
from .forms import *
from addresses.models import Address
from billing.models import BillingProfile, Card
from orders.models import Order
from bot.views import send_message_to_channel


class UserProductHistoryView(LoginRequiredMixin, ListView):
	template_name = "products/user-history.html"

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['products/mobile/user-history.html']
		else:
			return ['products/desktop/user-history.html']

	def get_queryset(self, *args, **kwargs):
		request = self.request
		views = request.user.objectviewed_set.by_model(Product, model_queryset=False)
		return views

class ProductDetailSlugView(ObjectViewedMixin, DetailView):

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['products/mobile/product-detail.html']
		else:
			return ['products/desktop/product-detail.html']

	def get_object(self, *args, **kwargs):
		slug = self.kwargs.get("slug")

		# For admins to be able to view not active items
		if self.request.user.is_authenticated():
			if self.request.user.is_admin:
				try:
					instance = Product.objects.get(slug=slug)
				except Product.DoesNotExist:
					raise Http404("Not found!")
				except Product.MultipleObjectsReturned:
					qs = Product.objects.filter(slug=slug)
					instance = qs.first()
				except:
					raise Http404("Hmm")
				return instance
		# normal case
		try:
			instance = Product.objects.get(slug=slug, active=True)
		except Product.DoesNotExist:
			raise Http404("Not found!")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active=True)
			instance = qs.first()
		except:
			raise Http404("Hmm")
		return instance

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs) 
		request = self.request
		user = request.user
		product = self.get_object()
		slug = self.kwargs.get('slug')
		images = ProductImage.objects.filter(slug=slug).order_by('image_order')
		context['images'] = images
		context['object_condition'] = product.condition.condition_eng
		context['region'] = product.user.region
		wishes = Wishlist.objects.filter(product=product).count() #counting all likes for a product
		context['likes'] = wishes
		context['report'] = _('Report?')
		context['size'] = _('Size:')
		context['condition'] = _('Condition:')
		context['description'] = _('Description:')
		context['btn_title'] = _('Contact seller')
		context['authentic'] = _('Authentic')
		context['verified'] = _('2-step-verified on')
		context['fake'] = _('Fake')
		context['checked_on'] = _('Checked on')
		context['ai_checked'] = _('AI-checked')
		context['to_be_approved'] = _('Needs to be approved by our expert team')
		context['posted'] = _('Posted')
		context['ago'] = _('ago')
		return context

	def post(self, request, *args, **kwargs):
		next_ = request.POST.get('next', '/')
		username = request.POST.get('chat_with', '/')
		redirect_url = next_ + 'messages/' + username
		return redirect(redirect_url)

class ProductCreateView(LoginRequiredMixin, RequestFormAttachMixin, CreateView):
	form_class = ImageForm

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get(self, request, *args, **kwargs):
		billing_profile, created = BillingProfile.objects.new_or_get(self.request)
		card, created = Card.objects.new_or_get(billing_profile=billing_profile)
		try:
			user_region = request.user.region.region_code
		except:
			msg_not_eligible = _("Only customers in Ukraine are eligible to sell (as for now)")
			messages.add_message(request, messages.WARNING, mark_safe(msg_not_eligible))
			return stay_where_you_are(request)
		if user_region != 'ua':
			msg_not_eligible = _("Only customers in Ukraine are eligible to sell (as for now)")
			messages.add_message(request, messages.WARNING, mark_safe(msg_not_eligible))
			return stay_where_you_are(request)


		if card.is_valid_card() == False:
			msg = _("Please add card information to add an item!")
			messages.add_message(request, messages.WARNING, mark_safe(msg))
			return redirect("accounts:user-update")

		brands = Brand.objects.all()
		brand_arr = []
		for brand in brands:
			brand_arr.append(str(brand))
		if request.is_ajax():
			json_data={
			'brand':brand_arr,
			}
			selected = self.request.GET.get('obj_id_gender', None)
			if selected is not None and selected is not '':
				selected_gender = Gender.objects.get(id=selected)
				category_list = Category.objects.filter(category_for = selected_gender)
				lookup_cat = (Q(undercategory_for=category_list.first()))
				for data_cat in category_list:
					lookup_cat = lookup_cat|Q(undercategory_for=data_cat)
				undercategory_list = Undercategory.objects.filter(lookup_cat)
				categories = [{
					"category":data.category,
					"id":data.id,
					"category_language":_(data.category_eng)
						}
						for data in category_list]
				undercategories = [{
					"undercategory_for":data.undercategory_for.category,
					"undercategory":data.undercategory,
					"id":data.id,
					'undercategory_language':_(data.undercategory_eng)
						}
						for data in undercategory_list] 
				json_data = {
						'categories':categories,
						'undercategories':undercategories
						}
				return JsonResponse(json_data)
			return JsonResponse(json_data)
		product_form = ImageForm(request)
		context={
		'form': product_form,
		'button': pgettext('Upload_Item_create', 'Create'),
		'title': _('Add a new item'),
		}

		context['overcategories'] = Overcategory.objects.all()
		context['genders'] = Gender.objects.all()
		context['categories'] = Category.objects.all().exclude(category_admin='KidsSize')
		context['undercategories'] = Undercategory.objects.all()
		context['categories_all'] = Category.objects.filter(category_for = Gender.objects.get(gender = 'Women'))
		context['conditions'] = Condition.objects.all()
		context['sizes'] = Size.objects.all()
		context['images_upload_limit'] = settings.IMAGES_UPLOAD_LIMIT
		return custom_render(request, 'products', 'product-create', context)

	def form_valid(self, form):
		request = self.request
		product = form.save()

		url = product.get_absolute_url()
		base_url = getattr(settings, 'BASE_URL', 'https://www.saltysalt.co')
		path = "{base}{path}".format(base=base_url, path=url)
		msg = _('Your item was checked by AI. Within next 24 hours the check will be confirmed by our moderator team and your item will be published')

		messages.add_message(request, messages.SUCCESS, msg)

		if self.request.is_ajax():	
			json_data={
						'url': url,
						'slug':product.slug
							}
			return JsonResponse(json_data)
		return redirect(url)

	def form_invalid(self, form):
		if self.request.is_ajax():

			return JsonResponse({'error':form.errors})
		context={
		'form': form,
		'button': pgettext('Upload_Item_create', 'Create'),
		'title':_('Add a new item')
		}
		context['images_upload_limit'] = settings.IMAGES_UPLOAD_LIMIT
		return render(self.request, 'products/product-create.html', context)

class AccountProductListView(LoginRequiredMixin, ListView):

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['products/mobile/my-items-list.html']
		else:
			return ['products/desktop/my-items-list.html']

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.by_user(request.user).order_by('-timestamp').active().available()

	def get_context_data(self, *args, **kwargs):
		context = super(AccountProductListView, self).get_context_data(*args,**kwargs)
		user = self.request.user
		return context

class ProductUpdateView(LoginRequiredMixin, UpdateView):
	form_class = ProductUpdateForm

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['products/mobile/product-create.html']
		else:
			return ['products/desktop/product-create.html']

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_form_kwargs(self):
		kwargs = super(ProductUpdateView, self).get_form_kwargs()
		kwargs['request'] = self.request
		slug = self.kwargs.get('slug')
		if slug is not None:
			kwargs['slug'] = slug
			product = Product.objects.get(slug=slug)
		return kwargs
	
	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		user = self.request.user
		try:
			instance = Product.objects.get(slug=slug, active=True, user=user)
		except Product.DoesNotExist:
			if self.request.user.is_admin == True: 
				instance = Product.objects.get(slug=slug, active=True)
			else:
				raise Http404("Not found!")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active=True, user=user)
			instance = qs.first()
		except:
			raise Http404("Hmm")
		#object_viewed_signal.send(instance.__class__, instance=instance, request=request)
		return instance

	def get_context_data(self, *args, **kwargs):
		context = super(ProductUpdateView, self).get_context_data(*args, **kwargs)
		request = self.request
		slug = self.kwargs.get('slug')
		context['overcategories'] = Overcategory.objects.all()
		context['genders'] = Gender.objects.all()
		context['categories'] = Category.objects.all()
		context['undercategories'] = Undercategory.objects.all()
		context['categories_all'] = Category.objects.filter(category_for = Gender.objects.get(gender = 'Women'))
		context['conditions'] = Condition.objects.all()
		context['sizes'] = Size.objects.all()
		context['object_slug'] = slug 
		context['title'] = _('Update')
		context['button']=_('Save')
		
		new_all_=[]
		all_ = ProductImage.objects.all().filter(slug=slug)
		for idx, image in enumerate(all_):
			new_all_.append(all_.filter(slug=slug,image_order=idx+1).first())
		context['images'] = new_all_
		return context

	def form_valid(self, form):
		request = self.request
		product = form.save()
		url = product.get_absolute_url()
		if self.request.is_ajax():	
			json_data={
						'url': url,
						'slug':product.slug
							}
			return JsonResponse(json_data)
		return redirect(url)

	def form_invalid(self, form):
		if self.request.is_ajax():
			return JsonResponse({'error':form.errors})
		context['images_upload_limit'] = settings.IMAGES_UPLOAD_LIMIT
		return render(self.request, 'products/product-create.html', context)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
	form_class = ProductCreateForm
	success_url = '/products/'

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['products/mobile/product-delete.html']
		else:
			return ['products/desktop/product-delete.html']

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		user = self.request.user
		try:
			instance = Product.objects.get(slug=slug, active=True, user=user)
		except Product.DoesNotExist:
			raise Http404("Not found!")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active=True, user=user)
			instance = qs.first()
		except:
			raise Http404("Hmm")
		return instance

@login_required
def product_delete(request):
	if request.user.is_authenticated():
		product_id=request.POST.get('product_id')
		user = request.user
		product_user = request.POST.get('user_product')
		if product_id is not None and str(user)==str(product_user):
			try:
				product_obj = Product.objects.get(id=product_id, user = user)
			except Product.DoesNotExist:
				return redirect("accounts:home")
			if product_obj.user == user:
				product_obj.delete()
				deleted = True
			if request.is_ajax():
				json_data={
					"deleted":deleted,
				}
				return JsonResponse(json_data, status=200)
		return redirect("products:user-list")
	else:
		return redirect('login')

@login_required
def product_report(request):
	product_id=request.POST.get('product_id')
	user = request.user
	previous = request.POST.get('previous', '/')

	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			return HttpResponseRedirect(previous)
		reported_product = ReportedProduct.objects.filter(user = user, product = product_obj)
		if reported_product.exists():
			messages.add_message(request, messages.SUCCESS, _("Thank you. We have already received your report."))
		else: 
			ReportedProduct.objects.create(user=user, product=product_obj)
			messages.add_message(request, messages.SUCCESS, _("Thank you. We will check this item manually."))
	return HttpResponseRedirect(previous)

class FakeProductsListView(LoginRequiredMixin, ListView):

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['products/mobile/fake-list.html']
		else:
			return ['products/desktop/fake-list.html']

	def get_queryset(self, *args, **kwargs):
		return Product.objects.fake()

	def get_context_data(self, *args, **kwargs):
		context = super(FakeProductsListView, self).get_context_data(*args,**kwargs)
		context['title'] = 'Detected fakes so far:'
		return context

class ProductCheckoutView(LoginRequiredMixin, RequestFormAttachMixin, UpdateView): 
	form_class = CheckoutMultiForm

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['products/mobile/checkout.html']
		else:
			return ['products/desktop/checkout.html']

	def get_product(self): # product
		qs = Product.objects.authentic().available().payable()
		id_ = self.kwargs.get('product_id')
		if id_.isdigit():
			products = qs.filter(id=id_)
			if products.exists():
				return products.first()
		return None

	def get_object(self): # user
		user = self.request.user
		try:
			self.region = user.region.region_code
		except:
			self.region = 'no region'
		if self.region == 'ua' or self.region == 'no region':
			if self.get_product() is not None: 
				product = self.get_product()
				if product.user != user: 
					self.product = self.get_product()
					return user 
		return None

	def get(self, request, *args, **kwargs):
		if self.get_object() is None:
			msg_not_available = _("The item you want to buy is not available anymore. Check out the others!")
			messages.add_message(request, messages.WARNING, mark_safe(msg_not_available))
			return redirect("products:list")
		return super(ProductCheckoutView,self).get(request, *args, **kwargs)

	def get_address(self):
		return Address.objects.filter(billing_profile__user=self.object).first()

	def get_success_url(self):
		return reverse("accounts:user-update")

	def get_context_data(self, *args, **kwargs):
		context = super(ProductCheckoutView, self).get_context_data(*args,**kwargs)
		context['title'] = _('Update your details')
		context['password_btn'] = _('Change password')
		context['buy_btn'] = _('Pay order')
		context['product'] = self.product
		return context

	def form_valid(self, form):
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(self.request)
		address = form['address_form'].save(commit=False)
		address.billing_profile = billing_profile
		address.save()
		order, created = Order.objects.new_or_get(billing_profile, self.product)
		order.shipping_address = address
		order.save()
		return redirect("payment:pay_view")


	def get_form_kwargs(self):
		kwargs = super(ProductCheckoutView, self).get_form_kwargs()
		kwargs.update(instance={
		    'address_form': self.get_address(),
		    # 'card_form': self.get_card(),
		})
		return kwargs


def make_authentic(request, *args, **kwargs):
	if request.user.is_authenticated() and request.user.is_admin:
		id_ = kwargs.get('id')
		product = Product.objects.get(id=id_)
		product.authentic = 'authentic'
		product.save()
		send_message_to_channel(product)
		return stay_where_you_are(request)





