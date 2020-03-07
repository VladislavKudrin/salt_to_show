
from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView
from django.http import JsonResponse

class SearchProductView(ListView):
	template_name = "search/view.html"

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			query=request.GET.get('q')
			filtered_products = []
			all_ = Product.objects.all().authentic().available()
			all_products= []
			for x in all_:
				all_products.append(x.title)
			json_data={
				"query": query,
				"filtered_products": all_products,
			}
			return JsonResponse(json_data, status=200)
		return super(SearchProductView, self).get(request, *args, **kwargs)


	def get_context_data(self,*args,**kwargs):
		user = self.request.user
		context=super(SearchProductView,self).get_context_data(*args,**kwargs)
		query=self.request.GET.get('q')
		context['query']=self.request.GET.get('q')
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		method_dict=request.GET
		query=method_dict.get('q', None)
		if query is not None:
			return Product.objects.search(query).order_by('-timestamp').authentic().available()
		return Product.objects.authentic().available()