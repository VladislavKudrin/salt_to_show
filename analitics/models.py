from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session

from accounts.signals import user_logged_in_signal
from .signals import object_viewed_signal
from .utils import get_client_ip



FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, 'FORCE_SESSION_TO_ONE', False)


User = settings.AUTH_USER_MODEL

class ObjectViewedQuerySet(models.query.QuerySet):
	def by_model(self, model_class, model_queryset=False):
		c_type = ContentType.objects.get_for_model(model_class)
		qs = self.filter(content_type=c_type)
		if model_queryset:
			viewed_ids = [x.object_id for x in qs]
			return model_class.objects.filter(pk__in=viewed_ids)
		return qs

class ObjectViewedManager(models.Manager):
	def get_queryset(self):
		return ObjectViewedQuerySet(self.model, using=self._db)

	def by_model(self, model_class, model_queryset=False):
		return self.get_queryset().by_model(model_class, model_queryset=model_queryset)

class ObjectViewed(models.Model):
	user 			= models.ForeignKey(User, blank=True, null=True) # User instance instance.id
	ip_adress 		= models.CharField(max_length=220, blank=True, null=True)
	content_type 	= models.ForeignKey(ContentType) # User, Product, Order, Cart, Adress
	object_id 		= models.PositiveIntegerField()	# User id, Product id, Order id
	content_object 	= GenericForeignKey('content_type', 'object_id') # Product instance
	timestamp 		= models.DateTimeField(auto_now_add=True)

	objects = ObjectViewedManager()

	def __str__(self):
		return "%s viewed %s" %(self.content_object, self.timestamp)


	class Meta:
		ordering = ['-timestamp'] #most recent saved show up first
		verbose_name = 'Object viewed'
		verbose_name_plural = 'Objects viewed'




def object_viewed_reciever(sender, instance, request, *args, **kwargs):
	c_type = ContentType.objects.get_for_model(sender) #instance.__class__
	user = None
	if request.user.is_authenticated():
		user = request.user
	filtered_queryset = ObjectViewed.objects.filter(
			user = user,
			content_type = c_type,
			object_id = instance.id,
			ip_adress = get_client_ip(request),
			)
	if not filtered_queryset.exists():
		new_view_obj = ObjectViewed.objects.create(
				user = user,
				content_type = c_type,
				object_id = instance.id,
				ip_adress = get_client_ip(request),
			)


object_viewed_signal.connect(object_viewed_reciever)


class UserSession(models.Model):
	user 			= models.ForeignKey(User, blank=True, null=True) # User instance instance.id
	ip_adress 		= models.CharField(max_length=220, blank=True, null=True)
	session_key		= models.CharField(max_length=100, blank=True, null=True)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	active 			= models.BooleanField(default=True)
	ended 			= models.BooleanField(default=False)

	def end_session(self):
		session_key = self.session_key
		
		try:
			Session.objects.get(pk=session_key)
			self.active = False
			self.ended = False
			self.save()
		except:
			pass
		return self.ended


def post_save_session_reciever(sender, instance, created, *args, **kwargs):
	if created:
		qs=UserSession.objects.filter(user=instance.user, ended=False,active=True).exclude(id=instance.id)
		for i in qs:
			i.end_session()
	if not instance.active and not instance.ended:
		instance.end_session()

if FORCE_SESSION_TO_ONE:
	post_save.connect(post_save_session_reciever, sender=UserSession)


def post_save_user_changed_reciever(sender, instance, created, *args, **kwargs):
	if not created:
		if instance.is_active == False:
			qs=UserSession.objects.filter(user=instance.user, ended=False,active=True).exclude(id=instance.id)
			for i in qs:
				i.end_session()


if FORCE_INACTIVE_USER_ENDSESSION:
	post_save.connect(post_save_user_changed_reciever, sender=User)


def user_logged_in_reciever(sender, instance, request, *args, **kwargs):
	user = instance
	session_key = request.session.session_key
	ip_adress = get_client_ip(request)
	UserSession.objects.create(
			user=user,
			ip_adress=ip_adress,
			session_key=session_key
		)


user_logged_in_signal.connect(user_logged_in_reciever)











