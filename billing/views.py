from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.conf import settings
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
# import stripe
# STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_1l8zkhQ1TSie6osuv340q2gy00sykrXaRe")
# STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY", 'pk_test_QZ1Bl6pNnSFwcWXaPOFaC2dx009AMrZvdk')
# stripe.api_key = STRIPE_SECRET_KEY
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from liqpay.liqpay3 import LiqPay
LIQPAY_PRIV_KEY = getattr(settings, "LIQPAY_PRIVATE_KEY", "sandbox_tLSKnsdkFbQgIe8eiK8Y2RcaQ3XUJl29quSa4aSG")
LIQPAY_PUB_KEY =  getattr(settings, "LIQPAY_PUBLIC_KEY", 'sandbox_i6955995458')
from .models import BillingProfile, Card
from orders.models import Order, Transaction


class PayView(TemplateView):
    template_name = 'billing/pay.html'
    def get(self, request, *args, **kwargs):
        liqpay = LiqPay(LIQPAY_PUB_KEY, LIQPAY_PRIV_KEY)
        callback_url = settings.BASE_URL_WITHOUT_WWW + reverse('payment:pay_callback')
        if settings.TESTMODE:
            callback_url = "https://en26sty6m4lpq.x.pipedream.net/"
        order = Order.objects.by_request(request).first()
        params = {
            "action"                : "hold",
            "version"               : "3",
            "phone"                 : "380950000001",
            "amount"                : str(order.convert_total(request.user)),
            "currency"              : "UAH",
            "description"           : "description text",
            "order_id"              : order.order_id,
            "letter_of_credit"      : "1",
            "letter_of_credit_date" : "2020-01-20 00:00:00",
            "server_url"            : callback_url, # url to callback view
            "recurringbytoken"      : "1",
            "result_url"            : settings.BASE_URL_WITHOUT_WWW + reverse('orders:list')
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data})

# @method_decorator(csrf_exempt, name='dispatch')
# class PayCallbackView(View):
#     def post(self, request, *args, **kwargs):
#         liqpay = LiqPay(LIQPAY_PUB_KEY, LIQPAY_PRIV_KEY)
#         data = request.POST.get('data')
#         signature = request.POST.get('signature')
#         sign = liqpay.str_to_sign(LIQPAY_PRIV_KEY + data + LIQPAY_PRIV_KEY)
#         if sign == signature:
#             response = liqpay.decode_data_from_str(data)
#             order_id = response.get("order_id")
#             order = Order.objects.filter(order_id=order_id)
#             if order.exists() and order.count() == 1:
#                 order = order.first()
#                 transaction = Transaction.objects.new_or_get(order=order, data=response)
#                 billing_profile = order.billing_profile
#                 if response.get("status") == "hold_wait":
#                     order.status = "hold_wait"
#                     order.save()
#                 else:
#                     transaction.transaction_error(data=response)
#                 if not billing_profile.has_card:
#                     card = Card.objects.create(billing_profile = billing_profile, card_token = response.get("card_token"))
#         return HttpResponse()
class PayCallbackView(APIView):
    def post(self, request):
        liqpay = LiqPay(LIQPAY_PUB_KEY, LIQPAY_PRIV_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
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
                    order.save()
                else:
                    transaction.transaction_error(data=response)
                if not billing_profile.has_card:
                    card = Card.objects.create(billing_profile = billing_profile, card_token = response.get("card_token"))
        return Response({"code":200})























def payment_method_view(request):
    #next_url = 
    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})




def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status_code=401)
        token = request.POST.get("token")
        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)
        return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse("error", status_code=401)
