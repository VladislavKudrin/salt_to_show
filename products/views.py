from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from django_file_form.uploader import FileFormUploader

from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin
from analitics.mixins import ObjectViewedMixin
from carts.models import Cart
from categories.models import Size

from accounts.models import User
from .models import Product, Image
from .forms import ProductCreateForm, ImageForm


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
		return context

	def post(self, request, *args, **kwargs):
		next_ = request.POST.get('next', '/')
		username = request.POST.get('chat_with', '/')
		redirect_url = next_ + 'dialogs/' + username
		return redirect(redirect_url)

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		
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



class ProductCreateView(LoginRequiredMixin, RequestFormAttachMixin, CreateView):
	form_class = ImageForm
	template_name = 'products/product-create.html'

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			selected = self.request.GET.get('selected')
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
		product_form = ImageForm(request)
		context={}
		context['title']='Create New Product'
		context['form']=product_form
		return render(request, 'products/product-create.html', context)
	def form_valid(self, form):
		product = form.save()
		url = product.get_absolute_url()
		return redirect(url)

class AccountProductListView(LoginRequiredMixin, ListView):
	template_name = 'products/user-list.html'
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.by_user(request.user)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
	form_class = ProductCreateForm
	template_name = 'products/product-update.html'
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
	product_id =request.POST.get('pk')
	product_obj = Product.objects.get(pk=product_id)
	request.user.wishes.add(product_obj)
	return redirect("accounts:home")


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
