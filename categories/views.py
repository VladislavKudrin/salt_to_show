from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.db.models import Q

from .models import Size, Brand
from products.models import Product




class CategoryFilterView(ListView):
	template_name = "categories/view.html"
	sizes = [
		Size.objects.filter(size_for='Footwear'),
		Size.objects.filter(size_for='Outwear'),
		Size.objects.filter(size_for='Tops'),
		Size.objects.filter(size_for='Bottoms'),
		Size.objects.filter(size_for='Accessories')
			]
	brands = Brand.objects.all()
	fields_category = [
					'footwear',
					'outwear',
					'tops',
					'bottoms',
					'accessories'
					]
	fields_gender = [
					'man',
					'woman',
					'unisex'
					]
	

	def post(self, request, *args, **kwargs):
		request = self.request
		context={}
		qs_category={}
		qs_gender={}
		qs_size={}
		qs_brand={}
		print(request.POST)
		for data in request.POST:
			for brand in self.brands:
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
		filtred_qs = Product.objects.by_category_gender(qs_category, qs_gender, qs_size, qs_brand)
		if filtred_qs is not None:
			context['object_list'] = filtred_qs
		else:
			context['object_list'] = Product.objects.all()
		
		context['filter_gender'] = qs_gender
		context['filter_size'] = qs_size
		context['filter_category'] = qs_category
		context['fields_category']=self.fields_category
		context['fields_gender']=self.fields_gender
		context['sizes']=self.sizes
		context['brands']=self.brands
		return render(self.request, "categories/view.html", context)


	def get(self, request, *args, **kwargs):
		context={}
		context['object_list']=Product.objects.all()
		context['fields_category']=self.fields_category
		context['fields_gender']=self.fields_gender
		context['sizes']=self.sizes
		context['brands']=self.brands
		return render(request, "categories/view.html", context)









