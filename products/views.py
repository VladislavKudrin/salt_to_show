from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin
from analitics.mixins import ObjectViewedMixin
from carts.models import Cart


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




# @login_required
# def product_create_view(request):
# 	Imageimage_form = modelimage_form_factory(Image,
# 										form=ImageForm, extra=3)
# 	if request.method == 'POST':
# 		productForm = ProductForm(request.POST)
# 		image_form = Imageimage_form(request.POST, request.FILES,
# 									queryset=Image.objects.none())
# 		if productForm.is_valid() and image_form.is_valid():
# 			product = postForm.save(commit=False)
# 			product.user = request.user
# 			product.save()
# 			for form in image_form.cleaned_data:
# 	image = form['image']
# 	photo = Images(post=post_form, image=image)
# 	photo.save()
# 	messages.success(request,
# 	"Posted!")
# 	return HttpResponseRedirect("/")
# 	else:
# 	print postForm.errors, image_form.errors
# 	else:
# 	postForm = PostForm()
# 	image_form = Imageimage_form(queryset=Images.objects.none())
# 	return render(request, 'index.html',
# 	{'postForm': postForm, 'image_form': image_form},
# 	context_instance=RequestContext(request))

# class BasePhotosimage_form(BaseModelimage_form):

    #By default, when you create a image_form from a model, the image_form
    #will use a queryset that includes all objects in the model

    # def __init__(self, *args, **kwargs):
    #     if 'city' in kwargs.keys():
    #         city = kwargs.pop('city')
    #     else:
    #         city = None
    #     super().__init__(*args, **kwargs)
    #     if city and isinstance(instance, Cities):
    #         self.queryset = Image.objects.filter(city=city)
    #     else:
    #         self.queryset = Description_Photos.objects.none()


class ProductCreateView(LoginRequiredMixin, CreateView):

	def post(self, request, *args, **kwargs): 
		product_form = ProductCreateForm(request.POST)
		image_form = ImageForm(request.POST, request.FILES)
		files = request.FILES.getlist('image')
		if product_form.is_valid() and image_form.is_valid():
			product = product_form.save(commit=False)
			product.user = request.user
			product.active = True
			product.save()
			for image in files:
				product_foto = Image(product=product, image=image)
				product_foto.save()
			return super(ProductCreateView, self).form_valid(product_form)

	def get(self, request, *args, **kwargs):
		product_form = ProductCreateForm()
		image_form = ImageForm(request.POST, request.FILES)
		context={}
		context['title']='Create New Product' #add kwarg / add your field for html
		context['product_form'] = product_form
		context['image_form'] = image_form
		return render(request, 'products/product-create.html', context)


	# def form_valid(self, form):
	# 	user = self.request.user
	# 	product = form.save()
	# 	product.user = user
	# 	product.active = True
	# 	product.save()
	# 	return super(ProductCreateView, self).form_valid(form)


	def get_context_data(self, *args, **kwargs): #overwriting default
		context = super(ProductCreateView, self).get_context_data(*args, **kwargs) #default method
		context['title']='Create New Product' #add kwarg / add your field for html
		return context
	

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




