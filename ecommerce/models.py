
from django.db.models.signals import post_save
from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore 
from django.contrib.sessions.backends.db import SessionStore

def session_post_save(sender, instance, created, *args, **kwargs):
	print('hello')


post_save.connect(session_post_save, sender=SessionStore)

