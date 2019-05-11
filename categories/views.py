from django.shortcuts import render
from django.views.generic import ListView



from products.models import Product



class CategoryFilterView(ListView):
	#queryset = Product.objects.all()
	template_name = "categories/view.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		all_ = request.GET.get('all', None)
		qs = {}
		qs_gender = {}
		man_ = request.GET.get('man', None)
		if man_ is not None:
			qs_gender['man'] = man_
		woman_ = request.GET.get('woman', None)
		if woman_ is not None:
			qs_gender['woman'] = woman_
		unisex_ = request.GET.get('unisex', None)
		if unisex_ is not None:
			qs_gender['unisex'] = unisex_
		if all_ is not None:
			return Product.objects.all()
		footwear_ = request.GET.get('footwear', None)
		if footwear_ is not None:
			qs['footwear']=footwear_
		outwear_ = request.GET.get('outwear', None)
		if outwear_ is not None:
			qs['outwear']=outwear_
		tops_ = request.GET.get('tops', None)
		if tops_ is not None:
			qs['tops']=tops_
		bottoms_ = request.GET.get('bottoms', None)
		if bottoms_ is not None:
			qs['bottoms']=bottoms_
		accessories_ = request.GET.get('accessories', None)
		if accessories_ is not None:
			qs['accessories']=accessories_
		print(qs)
		filtred_qs = Product.objects.by_category_gender(qs,qs_gender)
		return filtred_qs






