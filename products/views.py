
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
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django_file_form.models import UploadedFile
from django_file_form.uploader import FileFormUploader
from django_file_form.forms import ExistingFile

from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin
from analitics.mixins import ObjectViewedMixin
from carts.models import Cart
from categories.models import Size, Brand

from accounts.models import User
from .models import Product, Image, ImageOrderUtil
from .forms import ProductCreateForm, ImageForm, ProductUpdateForm

from django.db.utils import OperationalError
format_list = [('', '(all)')]
geom_type_list = [('', '(all)')]
try:
    format_list.extend([(i[0],i[0]) 
        for i in Product.objects.values_list('size')])
except OperationalError:
    pass  # happens when db doesn't exist yet, views.py should be
          # importable without this side effect


from django import template

register = template.Library()

@register.filter
def to_none(value):
    return ""


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
	#template_name = "products/list.html"

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(ProductListView, self).get_context_data(*args, **kwargs)
	##super обращается к классу-родителю, вызывает родитель-метод get_context_data
	# 	print(context)
	# 	return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		views = request.user.objectviewed_set.by_model(Product, model_queryset=False) #.filter(content_type='product') #reverse relationship with ForeignKey
		print(views)
		#viewed_ids = [x.object_id for x in views]
		# viewed_ids=[]
		# for x in views:
		# 	views_ids.append(x.object_id)
		return views
		
	def get_context_data(self, *args, **kwargs): #overwrite method
		context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)  #default method
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart']=cart_obj
		return context

class ProductListView(ListView):
	#queryset = Product.objects.all()
	template_name = "products/list.html"

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(ProductListView, self).get_context_data(*args, **kwargs)
	##super обращается к классу-родителю, вызывает родитель-метод get_context_data
	# 	print(context)
	# 	return contex
	def get_queryset(self, *args, **kwargs):
		qs = Product.objects.all()
		return qs
		
	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs) 
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart']=cart_obj
		return context



def product_list_view(request):
	queryset = Product.objects.all()
	context = {
		'object_list': queryset
	}
	return render(request, "products/list.html", context)


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs) 
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart']=cart_obj
		new_all_=[]
		request = self.request
		slug = self.kwargs.get('slug')
		all_ = Image.objects.all().filter(slug=slug)
		for idx, image in enumerate(all_):
			new_all_.append(all_.filter(slug=slug,image_order=idx+1).first())
		context['images'] = new_all_
		return context

	def post(self, request, *args, **kwargs):
		next_ = request.POST.get('next', '/')
		username = request.POST.get('chat_with', '/')
		redirect_url = next_ + 'dialogs/' + username
		return redirect(redirect_url)

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


class ProductDetailView(ObjectViewedMixin, DetailView):
	#queryset = Product.objects.all()
	template_name = "products/detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		instance = Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product doesnt Exist")
		return instance

	# def get_queryset(self, *args, **kwargs):
	# 	request = self.request
	# 	pk = self.kwargs.get('pk')
	# 	return Product.objects.filter(pk=pk)



def product_detail_view(request, pk=None, *args, **kwargs):
	#instance = Product.objects.get(pk=pk)
	#instance = get_object_or_404(Product, pk=pk)
	# try:
	# 	instance=Product.objects.get(id=pk)
	# except Product.DoesNotExist:
	# 	print('no product here')
	# 	raise Http404("Product doesnt Exist")
	# except:
	# 	print('huh?')
	instance = Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product doesnt Exist")
	# print(instance)
	# qs=Product.objects.filter(id=pk)
	# #print(qs)
	# if qs.exists() and qs.count()==1:
	# 	instance = qs.first()
	# else:
	# 	raise Http404("Product doesnt Exist")




	context = {
		'object': instance
	}
	return render(request, "products/detail.html", context)

def image_create_order(request):
	if request.POST:
		data = request.POST.getlist('data[]')
		slug = request.POST.get('slug')
		images = Image.objects.filter(slug=slug)
		array = numpy.array(data)
		array = array.astype(numpy.int)
		array = array + 1
		for img in images:
			min_ = min(array)
			index_of_min = numpy.where(array==min(array))[0][0].item()
			number = index_of_min + 1
			img.image_order=number
			print(img.image_order)
			array[index_of_min]=max(array)+1
			img.save()
	return redirect('home')


def image_update_view(request):
	if request.POST:
		data = request.POST.getlist('data[]')
		for idx, image_key in enumerate(data):
			Image.objects.filter(unique_image_id=image_key).update(image_order=idx+1)
	return redirect('home')


class ProductCreateView(LoginRequiredMixin, RequestFormAttachMixin, CreateView):
	form_class = ImageForm
	template_name = 'products/product-create.html'
	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			print('works')
			form = self.get_form()
			if form.is_valid():
				return self.form_valid(form)
			else:
				errors = form.errors
				# HttpResponse(json.dumps(errors), status=404)
				json_data={
						'error':errors
				}
				return JsonResponse(json_data, status=404)
	
	def get(self, request, *args, **kwargs):
		brands = Brand.objects.all()
		brand_arr = []
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
		context={}
		context['button']='Create'
		context['title']='Create New Product'
		context['form']=product_form

		return render(request, 'products/product-create.html', context)
	def form_valid(self, form):
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
		context={
			'form': form,
			'button': 'Create',
			'title':'Create New Product'
		}
		return render(self.request, 'products/product-create.html', context)


class AccountProductListView(LoginRequiredMixin, ListView):
	template_name = 'products/user-list.html'
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.by_user(request.user)


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
		context['title'] = 'Update'
		context['button']='Update' 
		new_all_=[]
		all_ = Image.objects.all().filter(slug=slug)
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


class WishListView(LoginRequiredMixin, ListView):
	template_name = 'products/wish-list.html'
	def get_queryset(self, *args, **kwargs):
		user = self.request.user
		wishes = user.wishes.all()
		pk_wishes = [x.pk for x in wishes] #['1', '3', '4'] / primary key list
		return Product.objects.filter(pk__in=wishes)




def wishlistupdate(request):
	product_id=request.POST.get('product_id')
	user = request.user
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Show message to user!")
			return redirect("products:wish-list")
		# cart_obj, new_obj = User.objects.get_or_create(request)
		if product_obj in user.wishes.all():
			user.wishes.remove(product_obj)
			added = False
		else:
			user.wishes.add(product_obj)
			added = True
		#request.session['cart_items']=cart_obj.products.count()
		if request.is_ajax():
			print("Ajax request YES")
			json_data={
				"added": added,
				"removed": not added,
				#"wishes":cart_obj.products.count()
			}
			return JsonResponse(json_data, status=200)
	return redirect("products:wish-list")


handle_upload = FileFormUploader()
