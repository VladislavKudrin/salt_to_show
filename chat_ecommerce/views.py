from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from datetime import datetime, timezone
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import DetailView, ListView

from .forms import ComposeForm
from .models import Thread, ChatMessage, Notification
from accounts.models import User

from products.models import Product


def set_chat_timezone(request):
    print('wtf')

class InboxView(LoginRequiredMixin, ListView):

    def get_template_names(self):
        if self.request.user_agent.is_mobile: 
            return ['chat_ecommerce/mobile/inbox.html']
        else:
            return ['chat_ecommerce/desktop/inbox.html']

    def get_queryset(self):
        return Thread.objects.by_recent_message(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        me = self.request.user
        threads_with_unred = Thread.objects.filter(chatmessage__notification__user=me, chatmessage__notification__read='False').distinct() # all threads with notifications where this specific request.user received notification! # filter by foreign key with multiple filters
        # filter by foreign key: здесь мы фильтруем треды по юзеру. затем по модели сообщения, 
        # которая не в атрибутах треда, а просто к нему привязана с форейн ки. Далее сообщение фильтруем по нотификэйшн,
        #  который тоже не указан в сообщениях, а лишь привязан к ней по форейн ки. 
        #  И далее по атрибуту у этого нотификэйшн рид=Фолс. 
        # Причем указывыаем просто  названия моделей.
        context['threads_with_unred'] = threads_with_unred
        context['chats'] = Thread.objects.by_recent_message(me)
        return context

class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    form_class = ComposeForm

    def get_template_names(self):
        if self.request.user_agent.is_mobile: 
            return ['chat_ecommerce/mobile/thread.html']
        else:
            return ['chat_ecommerce/desktop/thread.html']

    def get_success_url(self):
        return self.request.path
    def get_queryset(self):
        return Thread.objects.by_recent_message(self.request.user)
    def get_object(self):
        other_username  = self.kwargs.get("username")
        product_slug  = self.kwargs.get("product_id")
        # product = Product.objects.filter(slug=product_slug, active = True)#authentic = authentic
        obj, created = Thread.objects.get_or_new(user = self.request.user, other_username = other_username, product_slug = product_slug)

        me = self.request.user
        unread_notifications = Notification.objects.filter(user=me, read=False).filter(message__thread=obj) #unred notifications for this specific thread
        if unread_notifications:  
            for i in range(len(unread_notifications)):
                unread_notifications[i].read = True
                unread_notifications[i].save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        me = self.request.user
        obj = self.object
        # threads_with_unred = Thread.objects.by_user(mee).filter(chatmessage__notification__read='False')
        # unread_notifications = Notification.objects.filter(user=me, read=False).filter(message__thread=obj) #unred notifications for this specific thread
        # filter by foreign key: здесь мы фильтруем треды по юзеру. затем по модели сообщения, 
        threads_with_unred = Thread.objects.filter(chatmessage__notification__user=me, chatmessage__notification__read='False').distinct() # all threads with notifications where this specific request.user received notification! # filter by foreign key with multiple filters
        context['threads_with_unred'] = threads_with_unred
        context['form'] = self.get_form()
        context['chat_messages_ordered'] = obj.chatmessage_set.all().order_by('pk')
        context['chats'] = Thread.objects.by_recent_message(self.request.user)

        if self.request.user != self.get_object().first:
            context['opposite_user'] = self.get_object().first
        if self.request.user == self.get_object().first:
            context['opposite_user'] = self.get_object().second

        if obj.product:
            print(obj.product, 'hi')
        # print(context['chats'])
         # = Thread.objects.filter(chatmessage__user__notification=1)
        # threads_with_unred_notifications = Thread.objects.filter(chatmessage__user=me)
        # bla = Thread.objects.filter(chatmessage__message='Hey').filter(chatmessage__notification__read='True') 
        # context['unread_notifications'] = Notification.objects.filter(user=me, read=False) # existing chats with other users
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        other_username_kwargs  = self.kwargs.get("username")
        other_username = User.objects.filter(username=other_username_kwargs)[0]
        user = self.request.user
        thread = self.get_object()
        message = form.cleaned_data.get("message")
        msg_created = ChatMessage.objects.create(user=user, thread=thread, message=message)
        notification_created = Notification.objects.create(message=msg_created, user=other_username, read=False)
        # CHECK FOR UNREAD NOTIFICATIONS OF OTHER USER THAT OLDER THAN 10 min
        # print('hui', Notification.objects.filter(user=other_username))
        #email_sent = send_email_chat(recepient=other_username, message=msg_created)
        return super().form_valid(form)









