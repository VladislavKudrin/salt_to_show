from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from datetime import datetime, date, timezone
from products.models import Product
from django.utils.timezone import now

class ThreadManager(models.Manager):
    # def by_user(self, user): 
    #     qlookup = Q(first=user) | Q(second=user)
    #     qlookup2 = Q(first=user) & Q(second=user)
    #     qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
    #     return qs

    def by_recent_message(self, user): #returns a query set by users + sorted by recent messages in the thread + not displaying empty threads
        # ----- user part -----
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        # ---- sorting by recent messages part ----
        threads_and_recent = {} # {'1': 25 Aug 2018, '2': 4 Mai 1990}; 
        for thread in qs: 
            messages = ChatMessage.objects.filter(thread=thread).order_by('-timestamp')
            # print('CHATMESSAGE FOR {thread}'.format(thread=thread), messages)
            if messages:  # by that we don't display empty threads
                recent_timestamp= messages.first().timestamp
                # print('FIRST', recent_timestamp)
                threads_and_recent[thread] = recent_timestamp
        # print('threads_and_recent', threads_and_recent)
        sorted_qs = sorted(threads_and_recent, key=threads_and_recent.get, reverse=True) #sorted queryset
        # print(sorted_)
        return sorted_qs

    def get_or_new(self, user, other_username, product_slug = None): # get_or_create
            username = user.username
            if product_slug is not None:
                lookup_product_for_users = Q(slug=product_slug) & Q(active=True) & (Q(user__username=other_username) | Q(user__username=username))
                product = Product.objects.filter(lookup_product_for_users)
                if product.exists():
                    product = product.first()
                else:
                    product = None
            else:
                product = product_slug
            if username == other_username:
                # print(other_username)
                # print('hui')
                # print(username)
                return None
            qlookup1 = Q(first__username=username) & Q(second__username=other_username) & Q(product=product)
            qlookup2 = Q(first__username=other_username) & Q(second__username=username) & Q(product=product)
            qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
            if qs.count() == 1:
                return qs.first(), False
            elif qs.count() > 1:
                return qs.order_by('timestamp').first(), False
            else:
                Klass = user.__class__
                user2 = Klass.objects.get(username=other_username)
                if user != user2:
                    obj = self.model(
                            first=user, 
                            second=user2,
                            product=product
                        )
                    obj.save()
                    return obj, True
                return None, False

class Thread(models.Model):
    first         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
    second        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated       = models.DateTimeField(auto_now=True)
    timestamp     = models.DateTimeField(auto_now_add=True)
    product       = models.ForeignKey(Product, null=True, blank=True)
    active        = models.BooleanField(default=True)
    
    objects       = ThreadManager()
    
    def get_absolute_url_first(self):
        if self.product:
            return reverse('chat:chat-thread-product', kwargs={"username":self.first.username, "product_id":self.product.slug})
        return reverse('chat:chat-thread', kwargs={"username":self.first.username})
        
    def get_absolute_url_second(self):
        if self.product:
            return reverse('chat:chat-thread-product', kwargs={"username":self.second.username, "product_id":self.product.slug})
        return reverse('chat:chat-thread', kwargs={"username":self.second.username})
    def __str__(self):
        return f'{self.first, self.second, self.product}' # if websocets don't work change back to self.id

class ChatMessage(models.Model):
    thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.message}'


    @property
    def is_today(self):
        stamp = self.timestamp.date()
        today = datetime.today().date()
        return stamp == today

class Notification(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'notification')
    message     = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    read        = models.BooleanField(default=False)
    sent        = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    updated_at  = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.id}'