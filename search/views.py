from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView
from django.http import JsonResponse
from django.utils.translation import gettext as _

class SearchProductView(ListView):
	qs = Product.objects.authentic().available().payable() 

	def get_template_names(self):
		if self.request.user_agent.is_mobile: 
			return ['search/mobile/search-view.html']
		else:
			return ['search/desktop/search-view.html']

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			query=request.GET.get('q')
			all_products_titles= list(self.qs.order_by('-timestamp').values_list('title', flat=True).distinct())
			json_data={
				"query": query,
				"filtered_products": all_products_titles,
			}
			return JsonResponse(json_data, status=200)
		return super(SearchProductView, self).get(request, *args, **kwargs)


	def get_context_data(self,*args,**kwargs):
		user = self.request.user
		context=super(SearchProductView,self).get_context_data(*args,**kwargs)
		query=self.request.GET.get('q')
		context['query']=self.request.GET.get('q')
		context['emptiness'] = _('Oops... No results for your query. Try another one!')
		return context

	def get_queryset(self, *args, **kwargs):
		query=self.request.GET.get('q', None)
		if query is not None:
			return self.qs.search(query).order_by('-timestamp')
		return self.qs.order_by('-timestamp')