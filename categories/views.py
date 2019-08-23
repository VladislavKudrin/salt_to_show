from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.db.models import Q
from django.template.loader import get_template
from django.http import Http404, JsonResponse



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
				if type_[0] == 'gender':
					data_gender_link = type_[1]
				if type_[0] == 'category':
					data_category_link = type_[1].split('+')
				if type_[0] == 'undercategory':
					data_undercategory_link = type_[1].split('+')
				if type_[0] == 'size':
					data_size_link = type_[1].split('+')
				if type_[0] == 'price':
					data_price_link = type_[1].split('+')
				if type_[0] == 'condition':
					data_condition_link = type_[1].split('+')
				if type_[0] == 'brand':
					data_brand_link = type_[1]
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
				list_size=data_size_link
				)
		qs = Product.objects.all().order_by('-timestamp')
		qs_cat={}
		qs_undercat={}
		if request.is_ajax():
			# if raw_link:
			# 	request.GET['overcategory']
			# 	request.GET['gender']
			# 	request.GET['category']
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
					list_size=data_size
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
					context['object_list']=qs.order_by('price')
				elif data_sort == 'low':
					context['object_list']=qs.order_by('-price')
				else:
					context['object_list']=qs.order_by('-timestamp')
			else:
				link_codiert = 'givemetheloot'
				context['object_list']=qs

			html_ = get_template("products/snippets/languages/product_lists_cont.html").render(request = request, context=context)
			json_data={
			'html':html_,
			'link':link_codiert,
			'count_items':qs.count()
			}
			return JsonResponse(json_data)
		fields_gender = Gender.objects.all()
		fields_category = Category.objects.all()
		fields_overcategory = Overcategory.objects.all()
		fields_undercategory = Undercategory.objects.all()
		fields_size = Size.objects.all()
		fields_condition = Condition.objects.all()
		fields_brand = Brand.objects.all()

		context['object_list']=qs_for_link.order_by('-timestamp')
		context['fields_category']=fields_category
		context['fields_gender']=fields_gender
		context['fields_overcategory']=fields_overcategory
		context['fields_undercategory']=fields_undercategory
		context['fields_size']=fields_size
		context['fields_condition']=fields_condition  
		# context['sizes']=sizes
		context['fields_brand']=fields_brand
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
		


