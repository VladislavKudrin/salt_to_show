from django.test import TestCase
from django.shortcuts import render, redirect
from liqpay.liqpay3 import LiqPay
from django.conf import settings
from orders.models import Order, Transaction
from billing.models import Card

LIQPAY_PRIV_KEY = getattr(settings, "LIQPAY_PRIVATE_KEY", "sandbox_tLSKnsdkFbQgIe8eiK8Y2RcaQ3XUJl29quSa4aSG")
LIQPAY_PUB_KEY =  getattr(settings, "LIQPAY_PUBLIC_KEY", 'sandbox_i6955995458')






def response_test(request):
	liqpay = LiqPay(LIQPAY_PUB_KEY, LIQPAY_PRIV_KEY)
	data = "eyJhY3Rpb24iOiJob2xkIiwicGF5bWVudF9pZCI6MTIwMjY1MDk1NSwic3RhdHVzIjoiaG9sZF93YWl0IiwidmVyc2lvbiI6MywidHlwZSI6ImhvbGQiLCJwYXl0eXBlIjoiY2FyZCIsInB1YmxpY19rZXkiOiJzYW5kYm94X2k2OTU1OTk1NDU4IiwiYWNxX2lkIjo0MTQ5NjMsIm9yZGVyX2lkIjoicmtwZ2xodGx2dCIsImxpcXBheV9vcmRlcl9pZCI6IjNINTE2VE43MTU3NzIyMTgyMzEyMzI2MCIsImRlc2NyaXB0aW9uIjoiZGVzY3JpcHRpb24gdGV4dCIsInNlbmRlcl9jYXJkX21hc2syIjoiNDI0MjQyKjQyIiwic2VuZGVyX2NhcmRfYmFuayI6IlRlc3QiLCJzZW5kZXJfY2FyZF90eXBlIjoidmlzYSIsInNlbmRlcl9jYXJkX2NvdW50cnkiOjgwNCwiaXAiOiIxMzQuMTAxLjUuMTg3IiwiY2FyZF90b2tlbiI6InNhbmRib3hfdG9rZW4iLCJhbW91bnQiOjAuMjMsImN1cnJlbmN5IjoiVUFIIiwic2VuZGVyX2NvbW1pc3Npb24iOjAuMCwicmVjZWl2ZXJfY29tbWlzc2lvbiI6MC4wMSwiYWdlbnRfY29tbWlzc2lvbiI6MC4wLCJhbW91bnRfZGViaXQiOjAuMjMsImFtb3VudF9jcmVkaXQiOjAuMjMsImNvbW1pc3Npb25fZGViaXQiOjAuMCwiY29tbWlzc2lvbl9jcmVkaXQiOjAuMDEsImN1cnJlbmN5X2RlYml0IjoiVUFIIiwiY3VycmVuY3lfY3JlZGl0IjoiVUFIIiwic2VuZGVyX2JvbnVzIjowLjAsImFtb3VudF9ib251cyI6MC4wLCJtcGlfZWNpIjoiNyIsImlzXzNkcyI6ZmFsc2UsImxhbmd1YWdlIjoicnUiLCJjcmVhdGVfZGF0ZSI6MTU3NzIyMTgyMzEyNCwibGV0dGVyX29mX2NyZWRpdF9kYXRlIjoxNTc5NDc4NDAwMDAwLCJ0cmFuc2FjdGlvbl9pZCI6MTIwMjY1MDk1NX0="
	signature = "e96M8bSykMWGvZ7pEWTSwqprHm8="
	sign = liqpay.str_to_sign(LIQPAY_PRIV_KEY + data + LIQPAY_PRIV_KEY)
	if sign == signature:
		response = liqpay.decode_data_from_str(data)
		order_id = response.get("order_id")
		order = Order.objects.filter(order_id=order_id)
		if order.exists() and order.count() == 1:
			order = order.first()
			transaction = Transaction.objects.new_or_get(order=order, data=response)
			billing_profile = order.billing_profile
			if response.get("status") == "hold_wait":
				order.status = "hold_wait"
				order.product.active = False
				order.product.save()
				order.save()
			else:
				transaction.transaction_error(data=response)
			if not billing_profile.has_card:
				card = Card.objects.create(billing_profile = billing_profile, card_token = response.get("card_token"))
		context = {
				"response":response
		}
	else:
		context = {}
	return render(request, "billing/test.html", context)
