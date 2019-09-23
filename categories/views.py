from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.db.models import Q
from django.template.loader import get_template
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Size, Brand, Undercategory, Overcategory, Gender, Category, Condition
from products.models import Product
from .forms import TranslateForm


class CategoryFilterView(ListView):
	template_name = "products/list.html"
	def post(self, request, *args, **kwargs):
		print(request.POST)


		# brands = Brand.objects.all()
		# request = self.request
		# context={}
		# qs_category={}
		# qs_gender={}
		# qs_size={}
		# qs_brand={}
		# for data in request.POST:
		# 	for brand in brands:
		# 		if str(brand) == data:
		# 			qs_brand[brand]=brand
		# 	for field in self.fields_gender:
		# 		if field == data:
		# 			qs_gender[data] = data
		# 	for field in self.fields_category:
		# 		if field == data:
		# 			qs_category[data]=data
		# lookups_sizes=(Q(size_for__iexact='nothing'))
		# for category in qs_category:
		# 	lookups_sizes=lookups_sizes|(Q(size_for__iexact=category))
		# qs_size_unfiltred = Size.objects.filter(lookups_sizes)
		# for data in request.POST:
		# 	for size in qs_size_unfiltred:
		# 		if str(size)==str(data): 
		# 			qs_size[size]=size
		# filtred_qs = Product.objects.by_category_gender(qs_category, qs_gender, qs_size, qs_brand).order_by('-timestamp')
		# sort_qs = request.POST.get('qs_for_sort')
		# if sort_qs is not None:
		# 	lookups_products=(Q(slug__iexact='nothing'))
		# 	sort_qs_list = request.POST.getlist('qs_for_sort_slug')
		# 	for i in sort_qs_list:
		# 		lookups_products=lookups_products|(Q(slug__iexact=i))
		# 	relevant = request.POST.get('relevant')
		# 	high_low = request.POST.get('high_low')
		# 	low_high = request.POST.get('low_high')
		# 	sort = relevant or high_low or low_high
		# 	filtred_qs = Product.objects.filter(lookups_products).order_by(sort)
		# if filtred_qs is not None:
		# 	context['object_list'] = filtred_qs
		# else:
		# 	context['object_list'] = Product.objects.all()
		# context['filter_gender'] = qs_gender
		# context['filter_size'] = qs_size
		# context['filter_category'] = qs_category
		# context['fields_category']=self.fields_category
		# context['fields_gender']=self.fields_gender
		# context['sizes']=sizes
		# if len(qs_size) != 0 :
		# 	size_for_cont = next(iter(qs_size)).size_for
		# 	context['size_posted'] = size_for_cont
		# context['brands']=brands

		return render(self.request, "products/list.html", {})


	def get(self, request, *args, **kwargs):
		context={}
		# undercategory_instance_context =[]
		# words_for_overcategory = ['just', 'simply']
		# words_for_gender = ['put', 'add', 'include', 'insert', 'giveit', 'adjust']
		# words_for_category = {'Tops': 'tasty', 'Bottoms': 'delicious', 'Shoes': 'palatable', 'Accessories': 'luscious', 'Outerwear': 'vkusno', 'DressesAndOveralls': 'succulent'}
		# words_for_category_reverse = {'tasty': 'Tops', 'delicious': 'Bottoms', 'palatable': 'Shoes', 'luscious': 'Accessories', 'vkusno': 'Outerwear', 'succulent': 'DressesAndOveralls'}
		# words_for_undercategory_reverse = {'salt': 'T-ShirtsAndPolos', 'pepper': 'TopsAndBody', 'cardamom': 'Shirts', 'anise': 'Sweaters', 'cinnamon': 'SweatshirtsAndHoodies', 'coriander': 'Jeans', 'cumin': 'Shorts', 'marinade': 'Sweatpants', 'curry': 'Pants', 'fennel': 'Rocks', 'garam': 'Sneakers', 'ginger': 'CasualShoes', 'nutmeg': 'Boots', 'paprika': 'Sandals', 'turmeric': 'HighHeels', 'spice': 'BugsAndLuggage', 'mace': 'Belts', 'chili': 'Scarves', 'cloves': 'Hats', 'garlic': 'JewerlyAndWatches', 'oregano': 'Wallets', 'rosemary': 'SocksAndUnderwear', 'thyme': 'Sunglasses', 'vanilla': 'Miscellaneous', 'basil': 'HeavyJacketsAndParkas', 'chives': 'LeatherJackets', 'dill': 'Coats', 'mint': 'JeansJackets', 'sage': 'LightJackets', 'fenugreek': 'Dresses', 'parsley': 'Overalls'}
		# words_for_undercategory = {'T-ShirtsAndPolos': 'salt', 'TopsAndBody': 'pepper', 'Shirts': 'cardamom', 'Sweaters': 'anise', 'SweatshirtsAndHoodies': 'cinnamon', 'Jeans': 'coriander', 'Shorts': 'cumin', 'Sweatpants': 'marinade', 'Pants': 'curry', 'Rocks': 'fennel', 'Sneakers': 'garam', 'CasualShoes': 'ginger', 'Boots': 'nutmeg', 'Sandals': 'paprika', 'HighHeels': 'turmeric', 'BugsAndLuggage': 'spice', 'Belts': 'mace', 'Scarves': 'chili', 'Hats': 'cloves', 'JewerlyAndWatches': 'garlic', 'Wallets': 'oregano', 'SocksAndUnderwear': 'rosemary', 'Sunglasses': 'thyme', 'Miscellaneous': 'vanilla', 'HeavyJacketsAndParkas': 'basil', 'LeatherJackets': 'chives', 'Coats': 'dill', 'JeansJackets': 'mint', 'LightJackets': 'sage', 'Dresses': 'fenugreek', 'Overalls': 'parsley'}
		items_per_page = 12
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
		qs_for_link = qs_for_link.order_by('-timestamp').authentic()
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
		qs = Product.objects.all().authentic().order_by('-timestamp')
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
				# 	qs = Product.objects.filter(overcategory=Overcategory.objects.get(id=int(request.GET.get(data))))
				# 	link_codiert = link_codiert + words_for_overcategory[int(request.GET.get(data))-1] + splitword_overcategory
				# data_undercategory = request.GET.getlist('undercategory')
				# data_size = request.GET.getlist('size')
				# for data in request.GET:
				# 	if data == 'overcategory':
				# 		qs = Product.objects.filter(overcategory=Overcategory.objects.get(id=int(request.GET.get(data))))
				# 		link_codiert = link_codiert + words_for_overcategory[int(request.GET.get(data))-1] + splitword_overcategory
				# 	if data == 'gender':
				# 		qs = qs.filter(sex=Gender.objects.get(id=int(request.GET.get(data))))
				# 		link_codiert = link_codiert + words_for_gender[int(request.GET.get(data))-1] + splitword_gender
				# 	if data == 'category':
				# 		qs_cat, link_codiert = Product.objects.filter_undercategory_size(qs=qs, list_category=request.GET.getlist(data), link_codiert = link_codiert)
				# 	if data == 'undercategory':
				# 		qs_undercat, link_codiert = Product.objects.filter_undercategory_size(qs=qs, list_undercategory=request.GET.getlist(data), link_codiert = link_codiert, words_for_undercategory=words_for_undercategory)
				# 	if data =='size':
				# 		qs, link_codiert = Product.objects.filter_undercategory_size(qs=qs, list_size=request.GET.getlist(data), link_codiert = link_codiert)
				if data_sort == 'high':
					qs=qs.order_by('price')
				elif data_sort == 'low':
					qs=qs.order_by('-price')
				else:
					qs=qs.order_by('-timestamp')
				object_list = qs
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
		# context['sizes']=sizes
		context['fields_brand']=fields_brand
		if self.request.session.get('language') == 'RU':
			context['kids_navbar'] = 'Дети'
			context['new_navbar'] = 'Свежее'
			context['hide_filters'] = 'Спрятать фильтры'
			context['found'] = 'Найдено'
			context['items'] = 'айтемов'
			context['sort_by'] = 'Сортировать по'
			context['new'] = 'Сначала новые'
			context['price_to_high'] = 'Сначала дешевые'
			context['price_to_low'] = 'Сначала дорогие'
			context['gender'] = 'Гендер'
			context['overcategory'] = 'Тип'
			context['category'] = 'Категория'
			context['all'] = 'Все'
			context['size'] = 'Размер'
			context['condition'] = 'Состояние'
			context['brand'] = 'Бренд'
			context['price'] = 'Цена'
		elif self.request.session.get('language') == 'UA':
			context['kids_navbar'] = 'Дiтi'
			context['new_navbar'] = 'Свiже'
			context['hide_filters'] = 'Сховати фільтри'
			context['found'] = 'Знайдено'
			context['items'] = 'айтемов'
			context['sort_by'] = 'Сортувати по'
			context['new'] = 'Спочатку новi'
			context['price_to_high'] = 'Спочатку дешеві'
			context['price_to_low'] = 'Спочатку дорогі'
			context['gender'] = 'Гендер'
			context['overcategory'] = 'Тип'
			context['category'] = 'Категорiя'
			context['all'] = 'Усi'
			context['size'] = 'Рoзмiр'
			context['condition'] = 'Стан'
			context['brand'] = 'Бренд'
			context['price'] = 'Цiна'
		else:
			context['kids_navbar'] = 'Kids'
			context['new_navbar'] = 'New'
			context['hide_filters'] = 'Hide Filters'
			context['found'] = 'Found'
			context['items'] = 'Items'
			context['sort_by'] = 'Sort by'
			context['new'] = 'New first'
			context['price_to_high'] = 'Low price first'
			context['price_to_low'] = 'High price first'
			context['gender'] = 'Gender'
			context['overcategory'] = 'Type'
			context['category'] = 'Category'
			context['all'] = 'All'
			context['size'] = 'Size'
			context['condition'] = 'Condition'
			context['brand'] = 'Brand'
			context['price'] = 'Price'

		return render(request, "products/list.html", context)


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
		# sizes_all = Size.objects.filter(size_admin='Kids')
		# for size in sizes_all:
		# 	size.size_type = Overcategory.objects.get(overcategory='Kids')
		# 	size.save()
			# Size.objects.create(size_for = 'Outerwear', size_admin = size.size_admin, size = size.size, size_type = Overcategory.objects.get(overcategory='Kids'))
			# Size.objects.create(size_for = 'DressesAndOveralls', size_admin = size.size_admin, size = size.size, size_type = Overcategory.objects.get(overcategory='Kids'))
			# Size.objects.create(size_for = 'Tops', size_admin = size.size_admin, size = size.size, size_type = Overcategory.objects.get(overcategory='Kids'))
			# Size.objects.create(size_for = 'Bottoms', size_admin = size.size_admin, size = size.size, size_type = Overcategory.objects.get(overcategory='Kids'))
			# size.delete()
		if request.POST:
			#overcategories
			for data in request.POST:
				for overcategory in Overcategory.objects.all():
					if data.split('_')[0] == overcategory.overcategory:
						if data.split('_')[1] == 'ru':
							overcategory.overcategory_ru = request.POST.get(data)
							overcategory.save() 
						elif data.split('_')[1] == 'en':
							overcategory.overcategory_eng = request.POST.get(data)
							overcategory.save() 
						elif data.split('_')[1] == 'ua':
							overcategory.overcategory_ua = request.POST.get(data)
							overcategory.save()
						elif data.split('_')[1] == 'main':
							overcategory.overcategory = request.POST.get(data)
							overcategory.save() 
			#gender
			for data in request.POST:
				for gender in Gender.objects.all():
					if data.split('_')[0] == gender.gender:
						if data.split('_')[1] == 'ru':
							gender.gender_ru = request.POST.get(data)
							gender.save() 
						elif data.split('_')[1] == 'en':
							gender.gender_eng = request.POST.get(data)
							gender.save() 
						elif data.split('_')[1] == 'ua':
							gender.gender_ua = request.POST.get(data)
							gender.save()
						elif data.split('_')[1] == 'main':
							gender.gender = request.POST.get(data)
							gender.save()
			#categories
			for data in request.POST:
				for category in Category.objects.all():
					if data.split('_')[0] == category.category:
						if data.split('_')[1] == 'ru':
							category.category_ru = request.POST.get(data)
							category.save() 
						elif data.split('_')[1] == 'en':
							category.category_eng = request.POST.get(data)
							category.save() 
						elif data.split('_')[1] == 'ua':
							category.category_ua = request.POST.get(data)
							category.save()
						elif data.split('_')[1] == 'main':
							category.category = request.POST.get(data)
							category.save() 
			#undercategories
			for data in request.POST:
				for undercategory in Undercategory.objects.all():
					if data.split('_')[0] == undercategory.undercategory:
						if data.split('_')[1] == 'ru':
							undercategory.undercategory_ru = request.POST.get(data)
							undercategory.save() 
						elif data.split('_')[1] == 'en':
							undercategory.undercategory_eng = request.POST.get(data)
							undercategory.save() 
						elif data.split('_')[1] == 'ua':
							undercategory.undercategory_ua = request.POST.get(data)
							undercategory.save()
						elif data.split('_')[1] == 'main':
							undercategory.undercategory = request.POST.get(data)
							undercategory.save()

	else:
		return redirect('home')
	return render(request, "categories/translate.html", context)
		


