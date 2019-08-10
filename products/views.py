
import numpy
from pathlib import Path
from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse, HttpResponse
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
import json
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings

from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin
from analitics.mixins import ObjectViewedMixin
from carts.models import Cart
from categories.models import Size, Brand

from accounts.models import User, Wishlist
from .models import Product, ProductImage, ImageOrderUtil, ProductThumbnail, ReportedProduct
from .forms import ProductCreateForm, ImageForm, ProductUpdateForm
from image_uploader.models import unique_form_id_generator
from django.core.mail import send_mail






class ProductFeaturedListView(ListView):
	#queryset = Product.objects.all()
	template_name = "products/list.html"
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all().featured()

class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
	queryset = Product.objects.all().featured()
	template_name = "products/featured-detail.html"

	# def get_queryset(self, *args, **kwargs):
	# 	request = self.request
	# 	return Product.objects.featured()

class UserProductHistoryView(LoginRequiredMixin, ListView):
	#queryset = Product.objects.all()
	template_name = "products/user-history.html"
	paginate_by = 10
	#template_name = "products/list.html"

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(ProductListView, self).get_context_data(*args, **kwargs)
	##super обращается к классу-родителю, вызывает родитель-метод get_context_data
	# 	print(context)
	# 	return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		views = request.user.objectviewed_set.by_model(Product, model_queryset=False)
		#.filter(content_type='product') #reverse relationship with ForeignKey
		#viewed_ids = [x.object_id for x in views]
		# viewed_ids=[]
		# for x in views:
		# 	views_ids.append(x.object_id)
		return views
		
	def get_context_data(self, *args, **kwargs): #overwrite method
		user = self.request.user
		# all_wishes = user.wishes_user.all()
		# wished_products = [wish.product for wish in all_wishes]
		context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)  #default method
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart']=cart_obj
		if self.request.session.get('language') == 'RU':
			context['title']='Недавно просмотренное'
		elif self.request.session.get('language') == 'UA':
			context['title']='Нещодавно переглянуте'
		else:
			context['title']='Viewed items'		
		# context['wishes'] = wished_products
		return context

def product_list_view(request):
	queryset = Product.objects.all()
	context = {
		'object_list': queryset.order_by('-timestamp')
	}
	return render(request, "products/list.html", context)

class ProductDetailSlugView(ObjectViewedMixin, DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get("slug")
		
		#instance = get_object_or_404(Product, slug=slug, active=True)
		try:
			instance = Product.objects.get(slug=slug, active=True)
		except Product.DoesNotExist:
			raise Http404("Not found!")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active=True)
			instance = qs.first()
		except:
			raise Http404("Hmm")

		#object_viewed_signal.send(instance.__class__, instance=instance, request=request)
		return instance

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs) 
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart']=cart_obj
		new_all_=[]
		request = self.request
		user = request.user
		product = self.get_object()
		wishes = Wishlist.objects.filter(product=product).count() #counting all likes for a product
		print('WISHES', wishes)
		context['likes'] = wishes
		# all_wishes = user.wishes_user.all()
		# wished_products = [wish.product for wish in all_wishes]
		slug = self.kwargs.get('slug')
		all_ = ProductImage.objects.all().filter(slug=slug)
		for idx, image in enumerate(all_):
			new_all_.append(all_.filter(slug=slug,image_order=idx+1).first())
		context['images'] = new_all_
		if self.request.session.get('language') == 'RU':
			context['report'] = 'Жалоба?'
		elif self.request.session.get('language') == 'UA':
			context['report'] = 'Скарга?'
		else:
			context['report'] = 'Report?'
		return context

	def post(self, request, *args, **kwargs):
		next_ = request.POST.get('next', '/')
		username = request.POST.get('chat_with', '/')
		redirect_url = next_ + 'messages/' + username
		return redirect(redirect_url)

def image_create_order(request):
	if request.POST:
		data = request.POST.getlist('data[]')
		slug = request.POST.get('slug')
		rotated = request.POST.get('rotate[]')
		images = ProductImage.objects.filter(slug=slug)
		array = numpy.array(data)
		array = array.astype(numpy.int)
		array = array + 1
		for img in images:
			min_ = min(array)
			index_of_min = numpy.where(array==min(array))[0][0].item()
			number = index_of_min + 1
			img.image_order=number
			array[index_of_min]=max(array)+1
			img.save()


		ProductThumbnail.objects.create_update_thumbnail(product=images.first().product)
	return redirect('home')

def image_update_view(request):
	if request.POST:
		data = request.POST.getlist('data[]')
		for idx, image_key in enumerate(data):
			image = ProductImage.objects.filter(unique_image_id=image_key)
			image.update(image_order=idx+1)
		ProductThumbnail.objects.create_update_thumbnail(product=image.first().product)
	return redirect('home')

class ProductCreateView(LoginRequiredMixin, RequestFormAttachMixin, CreateView):
	form_class = ImageForm
	template_name = 'products/product-create.html'
	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

			# errors = form.errors
			# # HttpResponse(json.dumps(errors), status=404)
			# response = JsonResponse({"error": "there was an error"})
			# response.status_code = 403
			# return(response)
			# return JsonResponse(form.errors.as_json(), status=400)

	def get(self, request, *args, **kwargs):
		brands = Brand.objects.all()
		brand_arr = []
		form_id = unique_form_id_generator()
		for brand in brands:
			brand_arr.append(str(brand))
		if request.is_ajax():
			json_data={
			'brand':brand_arr,
			}
			selected = self.request.GET.get('selected', None)
			if selected == "select a category":
				selected = None
			if selected is not None:
				qs = Size.objects.filter(size_for__iexact=selected)
				sizes = [{
						"size": data.size,
						"id":data.id 
						} 
						for data in qs]
				json_data={
						'sizes': sizes
							}
				return JsonResponse(json_data)
			return JsonResponse(json_data)
		product_form = ImageForm(request)
		if self.request.session.get('language') == 'RU':
			context={
			'form': product_form,
			'button': 'Залить',
			'title':'Добавить новый айтем',
			'form_id': form_id
			}
		else:
			context={
			'form': product_form,
			'button': 'Create',
			'title':'Add a new product',
			'form_id': form_id
			}
		context['images_upload_limit'] = settings.IMAGES_UPLOAD_LIMIT
		return render(request, 'products/product-create.html', context)
	def form_valid(self, form):
		request = self.request
		product = form.save()
		url = product.get_absolute_url()

		base_url = getattr(settings, 'BASE_URL', 'https://www.saltysalt.co')
		path = "{base}{path}".format(base=base_url, path=url)

		#Message after upload
		subject = 'New item upload'
		message = 'New product was uploaded. Please verify authenticity: \n {} \n Product Title: {} \n Product Description: \n {}'.format(path, product.title, product.description)
		from_email = settings.DEFAULT_FROM_EMAIL
		to_email = settings.DEFAULT_FROM_EMAIL
		send_mail(subject, message, from_email, [to_email], fail_silently=False)

		if request.session.get('language')=='RU':
			msg = 'Твой айтем проверен Иcкусственным Интеллектом. В течение 24 часов проверку подтвердит модератор и айтем будет выставлен на продажу'
		# elif request.session.get('language')=='UA':
		else: 
			msg = 'Your item was checked by AI. Within next 24 hours the check will be confirmed by our moderator team and your item will be published'
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
			# json_data={
			# 	'errors':json.dumps(form.errors)
			# 	}
			return JsonResponse({'error':form.errors})
		if self.request.session.get('language') == 'RU':
			context={
			'form': form,
			'button': 'Залить',
			'title':'Добавить новый айтем',
			}
		else:
			context={
			'form': form,
			'button': 'Create',
			'title':'Add a new product'
			}
		context['images_upload_limit'] = settings.IMAGES_UPLOAD_LIMIT
		return render(self.request, 'products/product-create.html', context)

class AccountProductListView(LoginRequiredMixin, ListView):
	template_name = 'products/user-list.html'
	paginate_by = 10
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.by_user(request.user).order_by('-timestamp')

	def get_context_data(self, *args, **kwargs):
		context = super(AccountProductListView, self).get_context_data(*args,**kwargs)
		user = self.request.user
		if self.request.session.get('language') == 'RU':
			context['title'] = 'Мои айтемы'
			context['emptiness'] = 'Пока что здесь пусто'
		elif self.request.session.get('language') == 'UA':
			context['title'] = 'Мої айтеми'
			context['emptiness'] = 'Пока що тут пусто'
		else:
			context['title'] = 'My items'
			context['emptiness'] = 'No items yet'
		return context

class ProductUpdateView(LoginRequiredMixin, UpdateView):
	form_class = ProductUpdateForm
	template_name = 'products/product-create.html'

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
		#instance = get_object_or_404(Product, slug=slug, active=True)
		try:
			instance = Product.objects.get(slug=slug, active=True, user=user)
		except Product.DoesNotExist:
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
		if self.request.session.get('language') == 'RU':
			context['title'] = 'Редактировать'
			context['button']='Сохранить' 
		elif self.request.session.get('language') == 'UA':
			context['title'] = 'Редагувати'
			context['button']='Зберегти' 
		else:
			context['title'] = 'Update'
			context['button']='Save'
		
		new_all_=[]
		all_ = ProductImage.objects.all().filter(slug=slug)
		for idx, image in enumerate(all_):
			new_all_.append(all_.filter(slug=slug,image_order=idx+1).first())
		context['images'] = new_all_
		return context

class ProductDeleteView(LoginRequiredMixin, DeleteView):
	form_class = ProductCreateForm
	template_name = 'products/product-delete.html'
	success_url = '/products/'
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

class ProductUserDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'products/product-delete.html'
	model = Product
	success_url='/products/list/'
	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		user = self.request.user
		#instance = get_object_or_404(Product, slug=slug, active=True)
		try:
			instance = Product.objects.get(slug=slug, active=True, user=user)
		except Product.DoesNotExist:
			raise Http404("Not found!")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active=True, user=user)
			instance = qs.first()
		except:
			raise Http404("Hmm")

		#object_viewed_signal.send(instance.__class__, instance=instance, request=request)
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
				print("Show message to user!")
				return redirect("accounts:home")
			if product_obj.user == user:
				product_obj.delete()
				deleted = True
			if request.is_ajax():
				print("Ajax request")
				json_data={
					"deleted":deleted,
				}
				#return JsonResponse({"message":"Error 400"}, status_code=400)
				return JsonResponse(json_data, status=200)
		return redirect("products:user-list")
	else:
		return redirect('login')

@login_required
def product_report(request):
	product_id=request.POST.get('product_id')
	user = request.user
	# print('SUCCESS REPORT WORKING')
	# product_obj = Product.objects.get(id=product_id)
	
	previous = request.POST.get('previous', '/')
		# return HttpResponseRedirect(next)
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			return HttpResponseRedirect(previous)
	# 	user_wishes_exist = user_wishes.filter(product=product_obj)
		reported_product = ReportedProduct.objects.filter(user = user, product = product_obj)
		if reported_product.exists():
			if request.session.get('language')=='RU':
				messages.add_message(request, messages.SUCCESS, 'Спасибо. Мы уже получили твою жалобу.')
			elif request.session.get('language')=='UA':
				messages.add_message(request, messages.SUCCESS, 'Дякуємо. Ми вже отримали твою скаргу.')
			else:
				messages.add_message(request, messages.SUCCESS, "Thank you. We have already received your report.")
	# 		user.wishes.remove(product_obj)
	# 		user_wishes_exist.first().delete()
	# 		added = False
	# 		user_wishes_exist=user_wishes.count()
		else: 
			ReportedProduct.objects.create(user=user, product=product_obj)
			if request.session.get('language')=='RU':
				messages.add_message(request, messages.SUCCESS, 'Спасибо. Мы проверим этот айтем мануально.')
			elif request.session.get('language')=='UA':
				messages.add_message(request, messages.SUCCESS, 'Дякуємо. Ми перевіримо цей айтем мануально.')
			else:
				messages.add_message(request, messages.SUCCESS, "Thank you. We will check this item manually.")
	# 		added = True
	# 	if request.is_ajax():
	# 		json_data={
	# 			"added": added,
	# 			"removed": not added,
	# 			 "wishes_count": user_wishes_exist,
	# 			 'product_likes': product_likes,
	# 		}
	# 		return JsonResponse(json_data, status=200)
	return HttpResponseRedirect(previous)

class FakeProductsListView(LoginRequiredMixin, ListView):
	template_name = 'products/fake-list.html'
	paginate_by = 10
	def get_queryset(self, *args, **kwargs):
		return Product.objects.fake()

	def get_context_data(self, *args, **kwargs):
		context = super(FakeProductsListView, self).get_context_data(*args,**kwargs)
		if self.request.session.get('language') == 'RU':
			context['title'] = 'Обнаруженные фейки:'
		elif self.request.session.get('language') == 'UA':
			context['title'] = 'Виявлені фейки:'
		else:
			context['title'] = 'Detected fakes:'
		return context







# @login_required
# def wishlistupdate(request):
# 	product_id=request.POST.get('product_id')
# 	user = request.user
# 	if product_id is not None:
# 		try:
# 			product_obj = Product.objects.get(id=product_id)
# 		except Product.DoesNotExist:
# 			print("Show message to user!")
# 			return redirect("products:wish-list")
# 		# cart_obj, new_obj = User.objects.get_or_create(request)
# 		if product_obj in user.wishes.all():
# 			user.wishes.remove(product_obj)
# 			added = False
# 		else:
# 			user.wishes.add(product_obj)
# 			added = True
# 		#request.session['cart_items']=cart_obj.products.count()
# 		if request.is_ajax():
# 			print("Ajax request YES")
# 			json_data={
# 				"added": added,
# 				"removed": not added,
# 				#"wishes":cart_obj.products.count()
# 			}
# 			return JsonResponse(json_data, status=200)
# 	return redirect("products:wish-list")

# def product_reported(request):
# 	return render(request, 'products/product-report.html', {})



# def product_delete(request):
# 	if request.user.is_authenticated():
# 		product_id=request.POST.get('product_id')
# 		user = request.user
# 		product_user = request.POST.get('user_product')
# 		if product_id is not None and str(user)==str(product_user):
# 			try:
# 				product_obj = Product.objects.get(id=product_id, user = user)
# 			except Product.DoesNotExist:
# 				print("Show message to user!")
# 				return redirect("accounts:home")
# 			if product_obj.user == user:
# 				product_obj.delete()
# 				deleted = True
# 			if request.is_ajax():
# 				print("Ajax request")
# 				json_data={
# 					"deleted":deleted,
# 				}
# 				#return JsonResponse({"message":"Error 400"}, status_code=400)
# 				return JsonResponse(json_data, status=200)
# 		return redirect("products:user-list")
# 	else:
# 		return redirect('login')


# class ProductListView(ListView):
# 	#queryset = Product.objects.all()
# 	template_name = "products/list.html"

# 	def get_queryset(self, *args, **kwargs):
# 		qs = Product.objects.authentic()
# 		return qs

# 	# def get_context_data(self, *args, **kwargs):
# 	# 	context = super(ProductListView, self).get_context_data(*args, **kwargs)
# 	##super обращается к классу-родителю, вызывает родитель-метод get_context_data
# 	# 	print(context)
# 	# 	return contex

		
# 	def get_context_data(self, *args, **kwargs):
# 		context = super(ProductListView, self).get_context_data(*args, **kwargs) 
# 		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
# 		context['cart']=cart_obj
# 		return context



# class ProductDetailView(ObjectViewedMixin, DetailView):
# 	#queryset = Product.objects.all()
# 	template_name = "products/detail.html"

# 	def get_context_data(self, *args, **kwargs):
# 		user = self.request.user
# 		all_wishes = user.wishes_user.all()
# 		wished_products = []
# 		for wish in all_wishes: 
# 			wished_products.append(wish.product)
# 		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
# 		context['wishes']= wished_products
# 		print(context)
# 		return context

# 	def get_object(self, *args, **kwargs):
# 		request = self.request
# 		pk = self.kwargs.get('pk')
# 		instance = Product.objects.get_by_id(pk)
# 		if instance is None:
# 			raise Http404("Product doesnt Exist")
# 		return instance

# 	def get_queryset(self, *args, **kwargs):
# 		request = self.request
# 		pk = self.kwargs.get('pk')
# 		return Product.objects.filter(pk=pk)



# def product_detail_view(request, pk=None, *args, **kwargs):
# 	user = self.request.user
# 	all_wishes = user.wishes_user.all()
# 	print(all_wishes)
# 	print('fdfdfd')
# 	wished_products = []
# 	for wish in all_wishes: 
# 		wished_products.append(wish.product)
# 	# context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
# 	instance = Product.objects.get_by_id(pk)
# 	if instance is None:
# 		raise Http404("Product doesnt Exist")
# 	print(instance)
# 	# qs=Product.objects.filter(id=pk)
# 	# #print(qs)
# 	# if qs.exists() and qs.count()==1:
# 	# 	instance = qs.first()
# 	# else:
# 	# 	raise Http404("Product doesnt Exist")


# 	context = {
# 		'object': instance,
# 		'wishes': wished_products
# 	}
# 	# print(context)
# 	return render(request, "products/detail.html", context)