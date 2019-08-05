from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.db.models import Q

from .models import Size, Brand, Undercategory, Overcategory, Gender, Category, Condition
from products.models import Product
from .forms import TranslateForm


class CategoryFilterView(ListView):
	template_name = "products/list.html"
	fields_category = [
					'footwear',
					'outerwear',
					'tops',
					'bottoms',
					'accessories'
					]
	fields_gender = [
					'man',
					'woman'
					]
	

	def post(self, request, *args, **kwargs):
		print(request.POST)
		# sizes = [
		# Size.objects.filter(size_for='Footwear'),
		# Size.objects.filter(size_for='Outerwear'),
		# Size.objects.filter(size_for='Tops'),
		# Size.objects.filter(size_for='Bottoms'),
		# Size.objects.filter(size_for='Accessories')
		# 	]
		brands = Brand.objects.all()
		request = self.request
		context={}
		qs_category={}
		qs_gender={}
		qs_size={}
		qs_brand={}
		for data in request.POST:
			for brand in brands:
				if str(brand) == data:
					qs_brand[brand]=brand
			for field in self.fields_gender:
				if field == data:
					qs_gender[data] = data
			for field in self.fields_category:
				if field == data:
					qs_category[data]=data
		lookups_sizes=(Q(size_for__iexact='nothing'))
		for category in qs_category:
			lookups_sizes=lookups_sizes|(Q(size_for__iexact=category))
		qs_size_unfiltred = Size.objects.filter(lookups_sizes)
		for data in request.POST:
			for size in qs_size_unfiltred:
				if str(size)==str(data): 
					qs_size[size]=size
		filtred_qs = Product.objects.by_category_gender(qs_category, qs_gender, qs_size, qs_brand).order_by('-timestamp')
		sort_qs = request.POST.get('qs_for_sort')
		if sort_qs is not None:
			lookups_products=(Q(slug__iexact='nothing'))
			sort_qs_list = request.POST.getlist('qs_for_sort_slug')
			for i in sort_qs_list:
				lookups_products=lookups_products|(Q(slug__iexact=i))
			relevant = request.POST.get('relevant')
			high_low = request.POST.get('high_low')
			low_high = request.POST.get('low_high')
			sort = relevant or high_low or low_high
			filtred_qs = Product.objects.filter(lookups_products).order_by(sort)
		if filtred_qs is not None:
			context['object_list'] = filtred_qs
		else:
			context['object_list'] = Product.objects.all()
		
		context['filter_gender'] = qs_gender
		context['filter_size'] = qs_size
		context['filter_category'] = qs_category
		context['fields_category']=self.fields_category
		context['fields_gender']=self.fields_gender
		context['sizes']=sizes
		if len(qs_size) != 0 :
			size_for_cont = next(iter(qs_size)).size_for
			context['size_posted'] = size_for_cont
		context['brands']=brands

		return render(self.request, "products/list.html", context)


	def get(self, request, *args, **kwargs):
		# sizes = [
		# Size.objects.filter(size_for='Footwear'),
		# Size.objects.filter(size_for='Outerwear'),
		# Size.objects.filter(size_for='Tops'),
		# Size.objects.filter(size_for='Bottoms'),
		# Size.objects.filter(size_for='Accessories')
		# 	]
		brands = Brand.objects.all()
		context={}
		context['object_list']=Product.objects.all().order_by('-timestamp')
		context['fields_category']=self.fields_category
		context['fields_gender']=self.fields_gender
		# context['sizes']=sizes
		context['brands']=brands
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
		


