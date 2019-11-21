from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model


from billing.models import BillingProfile
from .models import Order, Transaction
from chat_ecommerce.models import Thread
from products.models import Product

User = get_user_model()

class OrderListView(LoginRequiredMixin, ListView):
	def get_queryset(self):
		return Order.objects.by_request(self.request).not_created()

class OrderDetailView(LoginRequiredMixin, DetailView):
	def get_object(self):
		qs = Order.objects.by_request(self.request).filter(
			order_id = self.kwargs.get('order_id')
					)
		if qs.count()==1:
			return qs.first()
		raise Http404


def transaction_initiation_view(request):
	if request.method == 'POST':
		opponent = User.objects.get(email=request.POST.get('opponent'))
		product = Product.objects.get(id=request.POST.get('product'))
		next_ = request.POST.get('next')
		thread_users = Thread.objects.filter(first = request.user, second = opponent, product = product, active=True) or Thread.objects.filter(second = request.user, first = opponent, product = product)
		if thread_users.exists():
			obj, created = Transaction.objects.get_or_create(thread = thread_users.first())
			print(obj, 'TRANSACTION')
	return redirect(next_)
