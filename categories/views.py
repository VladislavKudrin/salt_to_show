from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.db.models import Q

from .models import Size, Brand
from products.models import Product




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
		sizes = [
		Size.objects.filter(size_for='Footwear'),
		Size.objects.filter(size_for='Outerwear'),
		Size.objects.filter(size_for='Tops'),
		Size.objects.filter(size_for='Bottoms'),
		Size.objects.filter(size_for='Accessories')
			]
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
		context['brands']=brands
		return render(self.request, "products/list.html", context)


	def get(self, request, *args, **kwargs):
		sizes = [
		Size.objects.filter(size_for='Footwear'),
		Size.objects.filter(size_for='Outerwear'),
		Size.objects.filter(size_for='Tops'),
		Size.objects.filter(size_for='Bottoms'),
		Size.objects.filter(size_for='Accessories')
			]
		brands = Brand.objects.all()
		context={}
		context['object_list']=Product.objects.all().order_by('-timestamp')
		context['fields_category']=self.fields_category
		context['fields_gender']=self.fields_gender
		context['sizes']=sizes
		context['brands']=brands
		return render(request, "products/list.html", context)




		


