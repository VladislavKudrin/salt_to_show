from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.conf import settings
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
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
PAY_USER_SECRET_KEY = getattr(settings, "PAY_USER_SECRET_KEY", '')
from .models import BillingProfile, Card
from orders.models import Order, Transaction
from analitics.utils import get_client_ip
import requests


class PayView(TemplateView):
    template_name = 'billing/pay.html'
    def get(self, request, *args, **kwargs):
        liqpay = LiqPay(LIQPAY_PUB_KEY, LIQPAY_PRIV_KEY)
        callback_url = settings.BASE_URL_WITHOUT_WWW + reverse('payment:pay_callback')
        if settings.TESTMODE:
            callback_url = "https://enbarnzipr23p.x.pipedream.net"
        order = Order.objects.by_request(request).first()
        billingprofile, created = BillingProfile.objects.new_or_get(request)
        if billingprofile:
            address = billingprofile.address.first().get_address()
        params = {
            "action"                : "p2p",
            "version"               : "3",
            "amount"                : str(order.convert_total(request.user)),
            "currency"              : "UAH",
            "description"           : address,
            "receiver_card"         : "5168742220852416",
            "order_id"              : order.order_id,
            "server_url"            : callback_url, # url to callback view
            "recurringbytoken"      : "1",
            "result_url"            : settings.BASE_URL_WITHOUT_WWW + reverse('orders:list')
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data})

@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
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
                if response.get("status") == "success":
                    order.status = "paid"
                    order.save()
                    if order.product:
                        order.product.active = False
                        order.product.save()
                        order.send_email()
                else:
                    transaction.transaction_error(data=response)
                # if not billing_profile.has_card:
                #     card = Card.objects.create(billing_profile = billing_profile, card_token = response.get("card_token"))
        return HttpResponse()




class PayToUserView(LoginRequiredMixin, View):
    template_name = 'billing/pay2user.html'
    
    # def get_ip(self):
    #     response = requests.get('https://api.ipify.org?format=json')
    #     if response.status_code == 200:
    #         ip = response.json().get('ip')
    #         return ip
    #     return None
    def get(self, request, *args, **kwargs):
        secret_key = self.kwargs.get("secret_key")
        if request.user.is_admin and secret_key == PAY_USER_SECRET_KEY:
            orders = Order.objects.filter(status='shipped', active=True)
            context={
                'orders':orders
            }
            return render(request, self.template_name, context)
        else:
            return redirect('home')
    def post(self, request, *args, **kwargs):
        secret_key = self.kwargs.get("secret_key")
        if request.user.is_admin and secret_key == PAY_USER_SECRET_KEY:
            order_id = request.POST.get('order_id')
            liqpay = LiqPay(LIQPAY_PUB_KEY, LIQPAY_PRIV_KEY)
            callback_url = settings.BASE_URL_WITHOUT_WWW + reverse('payment:pay2user_callback')
            if settings.TESTMODE:
                callback_url = "https://enbarnzipr23p.x.pipedream.net"
            order = Order.objects.filter(order_id=order_id)
            if order.exists():
                order = order.first()
                seller_billing_profile = order.get_seller().billing_profile
                params = {
                    "action"                : "p2p",
                    "version"               : "3",
                    "amount"                : str(order.convert_total(order.get_seller())),
                    "currency"              : "UAH",
                    "description"           : order.product.title,
                    "receiver_card"         : seller_billing_profile.card.first().number,
                    "order_id"              : order.order_id+'complete',
                    "server_url"            : callback_url, # url to callback view
                    "recurringbytoken"      : "1",
                    "result_url"            : settings.BASE_URL_WITHOUT_WWW + reverse('payment:pay2user',kwargs={'secret_key':secret_key})
                }
                signature = liqpay.cnb_signature(params)
                data = liqpay.cnb_data(params)
                return render(request, 'billing/pay.html', {'signature': signature, 'data': data})
        return redirect('payment:pay2user')






@method_decorator(csrf_exempt, name='dispatch')
class PayToUserCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(LIQPAY_PUB_KEY, LIQPAY_PRIV_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(LIQPAY_PRIV_KEY + data + LIQPAY_PRIV_KEY)
        if sign == signature:
            response = liqpay.decode_data_from_str(data)
            order_id = response.get("order_id").split('complete')[0]
            order = Order.objects.filter(order_id=order_id)
            if order.exists() and order.count() == 1:
                order = order.first()
                transaction = Transaction.objects.new_or_get(order=order, data=response)
                if response.get("status") == "success":
                    order.active = False
                    order.save()
                    if order.product:
                        order.product.active = False
                        order.product.save()
                else:
                    transaction.transaction_error(data=response)
                    context={
                    'error_response':response,
                    'order_id':order_id
                    }
                    txt_ = get_template("billing/emails/payback_failure.txt").render(context)
                    html_ = get_template("billing/emails/payback_failure.html").render(context)
                    subject = ('Payment Failure: ' + order_id)
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [settings.DEFAULT_FROM_EMAIL]
                    sent_mail=send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message=html_,
                    fail_silently=False, 
                    )
                # if not billing_profile.has_card:
                #     card = Card.objects.create(billing_profile = billing_profile, card_token = response.get("card_token"))
        return HttpResponse()












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
