from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from billing.models import BillingProfile
from .models import Order, Transaction

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
	print(request.POST)
	next_ = request.POST.get('next')
	return redirect(next_)
