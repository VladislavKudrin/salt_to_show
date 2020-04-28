import json


from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import ListView
from django.db.models import Q
from django.template.loader import get_template
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext as _

from .models import Size, Brand, Undercategory, Overcategory, Gender, Category, Condition
from products.models import Product
from .forms import TranslateForm
from .utils import link_to_data
from ecommerce.utils import custom_render







class CategoryFilterView(ListView):

	def post(self, request, *args, **kwargs):
		return custom_render(request, "products", "product-list", {})

	def get(self, request, *args, **kwargs):
		context={}
		items_per_page = 32
		link_codiert = ''
		link = self.kwargs.get('filter')
		if link is not None:
			linked_data = link_to_data(link)
			queryset, context = Product.objects.get_categoried_queryset(request=request, linked_data=linked_data)
			queryset=queryset.authentic().available().prefetch_related('thumbnail')
		else:
			queryset = Product.objects.select_related('brand').select_related('size').all().authentic().available().order_by('-timestamp').prefetch_related('thumbnail')
		paginator = Paginator(queryset, items_per_page) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			queryset = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			queryset = paginator.page(1)
		except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
			queryset = paginator.page(paginator.num_pages)
		if request.is_ajax():
			page_continue = True
			context={}
			if request.GET:
				print('hallo')
				#getting queryset and link as json
				queryset, link_codiert = Product.objects.get_categoried_queryset(request=request)
				queryset = queryset.authentic().available()
				paginator = Paginator(queryset, items_per_page) 
				page = request.GET.get('page')
				try:
					queryset = paginator.page(page)
				except PageNotAnInteger:
					# If page is not an integer, deliver first page.
					queryset = paginator.page(1)
				except EmptyPage:
						# If page is out of range (e.g. 9999), deliver last page of results.
					queryset = paginator.page(paginator.num_pages)
				empty_price = all(minmax is '' for minmax in request.GET.getlist('price'))
				if page:
					if int(page) > paginator.num_pages:
						page_continue = False				
			context['object_list']=queryset
			if request.user_agent.is_mobile:
				html_ = get_template("products/snippets/mobile/card-product-list.html").render(request = request, context=context)
			else: 
				html_ = get_template("products/snippets/languages/product_lists_cont.html").render(request = request, context=context)
			json_data={
			'html':html_,
			'link':link_codiert,
			'count_pages': page_continue
			}
			return JsonResponse(json_data)
		fields_overcategory = Overcategory.objects.all()	
		fields_gender = Gender.objects.all().select_related('gender_for')
		fields_category = Category.objects.all().select_related('category_for')
		fields_undercategory = Undercategory.objects.all().select_related('undercategory_for')
		fields_size = Size.objects.all().select_related('size_type')
		fields_condition = Condition.objects.all()
		fields_brand = Brand.objects.all()
		context['fields_category']=fields_category
		context['fields_gender']=fields_gender
		context['fields_overcategory']=fields_overcategory
		context['fields_undercategory']=fields_undercategory
		context['fields_size']=fields_size
		context['fields_condition']=fields_condition  
		context['fields_brand']=fields_brand
		context['object_list']=queryset
		context['hide_filters'] = _('Hide Filters')
		context['show_filters'] = _('Show Filters')
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
		context['default_currency'] = settings.DEFAULT_CURRENCY
		return custom_render(request, "products", "product-list", context)

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
		


