from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, View
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse


from ecommerce.mixins import RequestFormAttachMixin
from billing.models import BillingProfile
from billing.forms import FeedbackForm
from .models import Order, Transaction
from .forms import OrderTrackForm

from chat_ecommerce.models import Thread
from products.models import Product
from django.core.urlresolvers import reverse

User = get_user_model()

class OrderListView(LoginRequiredMixin, View):
	template_name = "orders/order_list.html"
	def get(self, *args, **kwargs):
		tab = self.request.GET.get('tab')
		context = {}
		orders_sold = Order.objects.by_request_sold(self.request)
		orders_buy = Order.objects.by_request(self.request).exclude(status="shipped").exclude(status='refunded')
		orders_refunded_sell = Order.objects.by_request_sold(self.request).filter(status='refunded')
		orders_refunded_buy = Order.objects.by_request(self.request).filter(status='refunded')
		orders_completed_sell = Order.objects.by_request_sold(self.request).filter(status='shipped')
		orders_completed_buy = Order.objects.by_request(self.request).filter(status='shipped')
		orders_refunded = orders_refunded_buy | orders_refunded_sell
		orders_completed = orders_completed_buy | orders_completed_sell
		context['form'] = FeedbackForm(self.request)
		context['tab'] = tab
		context['orders_sold'] = orders_sold.filter(status='paid')
		context['orders_buy'] = orders_buy
		context['orders_refunded'] = orders_refunded.distinct()
		context['orders_completed'] = orders_completed.distinct()

		return render(self.request, self.template_name, context)

class OrderDetailView(LoginRequiredMixin, DetailView):
	def get_object(self):
		qs = Order.objects.by_request(self.request).filter(
			order_id = self.kwargs.get('order_id')
					)
		if qs.count()==1:
			return qs.first()
		raise Http404

def order_delete_view(request):
	if request.POST:
		order_id = request.POST.get('order_id')
		user_orders = Order.objects.by_request(request).filter(order_id=order_id, status='created')
		if user_orders.exists():
			order = user_orders.first()
			order.delete()
			if request.is_ajax():
				return HttpResponse('')
		return redirect('orders:list')
	else:
		return redirect('orders:list')

def order_complete_view(request):
	if request.POST:
		order_id = request.POST.get('order_id')
		user_orders = Order.objects.by_request(request).exclude(status='shipped').filter(order_id=order_id)
		if user_orders.exists():
			order = user_orders.first()
			order.complete_this_order(request)
			if request.is_ajax():
				json_data={
			'order_id':order.order_id
			}
				return JsonResponse(json_data)
		return redirect('orders:list')
	else:
		return redirect('orders:list')

def order_give_feedback(request):
	if request.POST:
		form = FeedbackForm(data=request.POST, request=request)
		if form.is_valid():
			form.save()
			if request.is_ajax():
				json_data={
			'next':reverse('orders:list')
			}
				return JsonResponse(json_data)
	return redirect('orders:list')


def order_track_view(request):
	if request.POST:
		track_number = request.POST.get('track_number')
		order_id = request.POST.get('order_id')
		user_orders = Order.objects.by_request_sold(request).filter(order_id=order_id)
		if user_orders.exists():
			order = user_orders.first()
			track_form = OrderTrackForm(request.POST, instance = order)
			if track_form.is_valid():
				track_form.save()
		link = reverse('orders:list') + '?tab=sold'
		return redirect(link)
	else:
		return redirect('orders:list')

# def transaction_initiation_view(request):
# 	if request.method == 'POST':
# 		opponent = User.objects.get(email=request.POST.get('opponent'))
# 		product = Product.objects.get(id=request.POST.get('product'))
# 		next_ = request.POST.get('next')
# 		thread_users = Thread.objects.filter(first = request.user, second = opponent, product = product, active=True) or Thread.objects.filter(second = request.user, first = opponent, product = product)
# 		if thread_users.exists():
# 			obj, created = Transaction.objects.get_or_create(thread = thread_users.first())
# 			print(obj, 'TRANSACTION')
# 	return redirect(next_)
