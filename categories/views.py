from django.shortcuts import render, redirect
from django.views.generic import ListView


from .models import Size
from products.models import Product



class CategoryFilterView(ListView):
	#queryset = Product.objects.all()
	sizes = Size.objects.all()
	print(sizes)
	template_name = "categories/view.html"
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
		for data in request.POST:
			for field in self.fields_gender:
				if field == data:
					qs_gender[data] = data
			for field in self.fields_category:
				if field == data:
					qs_category[data]=data
		print(qs_gender)
		print(qs_category)
		filtred_qs = Product.objects.by_category_gender(qs_category, qs_gender)
		if filtred_qs is not None:
			context['object_list'] = filtred_qs
		context['fields_category']=self.fields_category
		context['fields_gender']=self.fields_gender
		context['sizes']=self.sizes
		return render(self.request, "categories/view.html", context)


	def get(self, request, *args, **kwargs):
		context={}
		context['fields_category']=self.fields_category
		context['fields_gender']=self.fields_gender
		context['sizes']=self.sizes
		return render(request, "categories/view.html", context)



	# def get_queryset(self, *args, **kwargs):
	# 	if self.request.POST:
	# 		print(self.filtered_qs_final)
	# 		print('inqs')
	# 	request = self.request
	# 	all_ = request.GET.get('all', None)
	# 	qs = {}
	# 	qs_gender = {}
	# 	man_ = request.GET.get('man', None)
	# 	if man_ is not None:
	# 		qs_gender['man'] = man_
	# 	woman_ = request.GET.get('woman', None)
	# 	if woman_ is not None:
	# 		qs_gender['woman'] = woman_
	# 	unisex_ = request.GET.get('unisex', None)
	# 	if unisex_ is not None:
	# 		qs_gender['unisex'] = unisex_
	# 	if all_ is not None:
	# 		return Product.objects.all()
	# 	footwear_ = request.GET.get('footwear', None)
	# 	if footwear_ is not None:
	# 		qs['footwear']=footwear_
	# 	outwear_ = request.GET.get('outwear', None)
	# 	if outwear_ is not None:
	# 		qs['outwear']=outwear_
	# 	tops_ = request.GET.get('tops', None)
	# 	if tops_ is not None:
	# 		qs['tops']=tops_
	# 	bottoms_ = request.GET.get('bottoms', None)
	# 	if bottoms_ is not None:
	# 		qs['bottoms']=bottoms_
	# 	accessories_ = request.GET.get('accessories', None)
	# 	if accessories_ is not None:
	# 		qs['accessories']=accessories_
	# 	print(qs)
	# 	filtred_qs = Product.objects.by_category_gender(qs,qs_gender)
	# 	return filtred_qs










