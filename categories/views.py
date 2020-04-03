from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.db.models import Q
from django.template.loader import get_template
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext as _

from .models import Size, Brand, Undercategory, Overcategory, Gender, Category, Condition
from products.models import Product
from .forms import TranslateForm
from ecommerce.utils import my_render


class CategoryFilterView(ListView):

	def post(self, request, *args, **kwargs):
		return my_render(request, "products", "list", {})

	def get(self, request, *args, **kwargs):
		context={}
		words_for_undercategory = {'T-ShirtsAndPolos': 'salt', 'TopsAndBody': 'pepper', 'Shirts': 'cardamom', 'Sweaters': 'anise', 'SweatshirtsAndHoodies': 'cinnamon', 'Jeans': 'coriander', 'Shorts': 'cumin', 'Sweatpants': 'marinade', 'Pants': 'curry', 'Rocks': 'fennel', 'Sneakers': 'garam', 'CasualShoes': 'ginger', 'Boots': 'nutmeg', 'Sandals': 'paprika', 'HighHeels': 'turmeric', 'BugsAndLuggage': 'spice', 'Belts': 'mace', 'Scarves': 'chili', 'Hats': 'cloves', 'JewerlyAndWatches': 'garlic', 'Wallets': 'oregano', 'SocksAndUnderwear': 'rosemary', 'Sunglasses': 'thyme', 'Miscellaneous': 'vanilla', 'HeavyJacketsAndParkas': 'basil', 'LeatherJackets': 'chives', 'Coats': 'dill', 'JeansJackets': 'mint', 'LightJackets': 'sage', 'Dresses': 'fenugreek', 'Overalls': 'parsley'}
		items_per_page = 32
		link_codiert = ''
		link = self.kwargs.get('filter')
		splitword_overcategory = 'please'
		splitword_gender = 'some'
		splitword_category = 'and'
		raw_link = False
		qs_for_link = Product.objects.all()
		if link is not None:
			words = link.split('&')
			data_brand_link=None
			data_price_link=None
			data_overcategory_link=None
			data_gender_link=None
			data_category_link=None
			data_undercategory_link=None
			data_size_link=None
			data_condition_link=None
			for word in words:
				type_ = word.split('=')
				if type_[0] == 'overcategory':
					data_overcategory_link = type_[1]
					if '/' in data_overcategory_link:
						data_overcategory_link= data_overcategory_link.replace('/', '')
				if type_[0] == 'gender':
					data_gender_link = type_[1]
					if '/' in data_gender_link:
						data_gender_link= data_gender_link.replace('/', '')
				if type_[0] == 'category':
					data_category_link = type_[1].split('+')
					if '/' in data_category_link:
						data_category_link= data_category_link.replace('/', '')
				if type_[0] == 'undercategory':
					data_undercategory_link = type_[1].split('+')
					if '/' in data_undercategory_link:
						data_undercategory_link= data_undercategory_link.replace('/', '')
				if type_[0] == 'size':
					data_size_link = type_[1].split('+')
					if '/' in data_size_link:
						data_size_link= data_size_link.replace('/', '')
				if type_[0] == 'price':
					data_price_link = type_[1].split('+')
					if '/' in data_price_link:
						data_price_link= data_price_link.replace('/', '')
				if type_[0] == 'condition':
					data_condition_link = type_[1].split('+')
					if '/' in data_condition_link:
						data_condition_link= data_condition_link.replace('/', '')
				if type_[0] == 'brand':
					data_brand_link = type_[1].split('+')
					if '/' in data_brand_link:
						data_brand_link= data_brand_link.replace('/', '')
			qs_for_link, trash, context = Product.objects.filter_from_link_or_ajax(
				qs=qs_for_link, 
				linked=True, 
				list_brand=data_brand_link, 
				list_condition=data_condition_link, 
				list_price=data_price_link,
				list_overcategory=data_overcategory_link,
				list_gender = data_gender_link, 
				list_category = data_category_link, 
				list_undercategory=data_undercategory_link, 
				list_size=data_size_link,
				user=request.user
				)
		qs_for_link = qs_for_link.order_by('-timestamp').authentic().available()
		paginator = Paginator(qs_for_link, items_per_page) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			qs_for_link = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			qs_for_link = paginator.page(1)
		except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
			qs_for_link = paginator.page(paginator.num_pages)
		qs = Product.objects.all().authentic().available().order_by('-timestamp')
		qs_cat={}
		qs_undercat={}
		if request.is_ajax():
			page_continue = True
			context={}
			if request.GET:
				data_brand = request.GET.getlist('brand')
				data_sort = request.GET.get('sort')
				data_price = request.GET.getlist('price')
				data_overcategory = request.GET.get('overcategory')
				data_gender = request.GET.get('gender')
				data_category = request.GET.getlist('category')
				data_undercategory = request.GET.getlist('undercategory')
				data_size = request.GET.getlist('size')
				data_condition = request.GET.getlist('condition')
				qs, link_codiert, con = Product.objects.filter_from_link_or_ajax(
					qs=qs, 
					list_brand = data_brand, 
					list_condition = data_condition,
					list_price=data_price,
					list_overcategory=data_overcategory,
					list_gender = data_gender, 
					list_category = data_category, 
					list_undercategory=data_undercategory, 
					list_size=data_size,
					user = request.user
					)
				if data_sort == 'high':
					qs=qs.order_by('price')
				elif data_sort == 'low':
					qs=qs.order_by('-price')
				else:
					qs=qs.order_by('-timestamp')
				object_list = qs.authentic().available()
				paginator = Paginator(object_list, items_per_page) 
				page = request.GET.get('page')
				try:
					object_list = paginator.page(page)
				except PageNotAnInteger:
					# If page is not an integer, deliver first page.
					object_list = paginator.page(1)
				except EmptyPage:
						# If page is out of range (e.g. 9999), deliver last page of results.
					object_list = paginator.page(paginator.num_pages)
				empty_price = all(minmax is '' for minmax in request.GET.getlist('price'))
				if len(request.GET)==1 and empty_price:
					link_codiert = 'all'
				if page:
					if int(page) > paginator.num_pages:
						page_continue = False
				context['object_list']=object_list
			else:
				context['object_list']=qs
			html_ = get_template("products/snippets/languages/product_lists_cont.html").render(request = request, context=context)
			json_data={
			'html':html_,
			'link':link_codiert,
			'count_items':qs.count(),
			'count_pages': page_continue
			}
			return JsonResponse(json_data)
		fields_gender = Gender.objects.all()
		fields_category = Category.objects.all()
		fields_overcategory = Overcategory.objects.all()
		fields_undercategory = Undercategory.objects.all()
		fields_size = Size.objects.all()
		fields_condition = Condition.objects.all()
		fields_brand = Brand.objects.all()
		brands_navbar_init = ['Gucci', 'Stone Island', 'Chanel', 'Prada', 'Louis Vuitton', 'Dolce & Gabbana', 'Yves Saint Laurent', 'Fendi', 'Burberry', 'Givenchy', 'Versace', 'Balenciaga', 'Giorgio Armani', 'C.P. Company', 'Calvin Klein', 'Balmain', 'Alexander Wang', 'Boss']
		brand_navbar_lookups = (Q(brand_name__iexact='nothing'))
		for brand in brands_navbar_init:
			brand_navbar_lookups = brand_navbar_lookups|(Q(brand_name__iexact=brand))
		context['showed_brands_navbar'] = Brand.objects.filter(brand_navbar_lookups)
		context['gender_navbar_adults'] = Gender.objects.filter(gender_for=Overcategory.objects.get(overcategory='Adults'))
		context['gender_navbar_kids'] = Gender.objects.filter(gender_for=Overcategory.objects.get(overcategory='Kids'))
		context['object_list']=qs_for_link
		context['fields_category']=fields_category
		context['fields_gender']=fields_gender
		context['fields_overcategory']=fields_overcategory
		context['fields_undercategory']=fields_undercategory
		context['fields_size']=fields_size
		context['fields_condition']=fields_condition  
		context['fields_brand']=fields_brand
		context['kids_navbar'] = _('Kids')
		context['new_navbar'] = _('New')
		context['hide_filters'] = _('Hide Filters')
		context['show_filters'] = _('Show Filters')
		context['found'] = _('Found')
		context['items'] = _('Items')
		context['sort_by'] = _('Sort by')
		context['new'] = _('New first')
		context['price_to_high'] = _('Low price first')
		context['price_to_low'] = _('High price first')
		context['gender'] = _('Gender')
		context['overcategory'] = _('Type')
		context['category'] = _('Category')
		context['all'] = _('All')
		context['size'] = _('Size')
		context['condition'] = _('Condition')
		context['brand'] = _('Brand')
		context['price'] = _('Price')
		return my_render(request, "products", "list", context)


def translation_view(request):
	context = {}
	if request.user.is_admin:
		cat_all_ = Category.objects.all().filter(category_for=Gender.objects.get(gender='Women'))
		lookups_undercat = (Q(undercategory_for=cat_all_.first()))
		for cat in cat_all_:
			lookups_undercat = lookups_undercat|Q(undercategory_for=cat)
		context['is_admin'] = 'true'
		translate_form=TranslateForm(request.POST or None)
		context['form'] = translate_form
		context['overcategories'] = Overcategory.objects.all()
		context['genders'] = Gender.objects.all().exclude(gender_for=Overcategory.objects.filter(overcategory='Kids'), gender='Gender-Neutral')
		context['categories'] = Category.objects.filter(category_for=Gender.objects.get(gender='Women'))
		context['undercategories'] = Undercategory.objects.filter(lookups_undercat)
		context['sizes'] = Size.objects.all()
		context['languages'] = {'ru':'ru',
								'ua':'ua',
								'en':'en'}
	return render(request, "categories/translate.html", context)
		


