import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage, Notification
from accounts.models import User
from django.forms.models import model_to_dict
from django.core import serializers
import itertools


class ChatConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		# when the socket connects
		# print('connected', event)
		other_user = self.scope['url_route']['kwargs']['username'] #get that username from url kwargs, kwargs coming from routing.py urls
		# other_user_full = User.objects.filter(username=other_user).first() #get user 
		me = self.scope['user'] # takes user this.username gives username / self.request.user
		try:
			product_slug = self.scope['url_route']['kwargs']['product_id']
		except:
			product_slug = None
		thread_obj, created = await self.get_thread(user = me, other_username = other_user, product_slug = product_slug) #get the thread

		self.thread_obj = thread_obj

		chat_room = f'thread_{thread_obj.id}' #get chat_room (=thread)
		# print(f'CHAT ROOM{chat_room}')
		self.chat_room = chat_room
		# await self.update_notification_status(me, thread_obj) #update notifications in this thread of current user
		await self.channel_layer.group_add(
			chat_room, #where to send
			self.channel_name #default attr from channels
			)
		await self.send({
			'type':'websocket.accept'
			})

	async def websocket_receive(self, event):
		# i = event
		# print(i)
		# current = await channels.auth.get_user(scope)
		# # when the socket connects
		# print(event)
		# print(current)
		# message_type = event.get('type', None)  #check message type, act accordingly
		# if message_type == "notification_read":
		# 	# Update the notification read status flag in Notification model.
		# 	notification = Notification.object.get(id=notification_id)
		# 	notification.notification_read = True
		# 	notification.save()  #commit to DB
		# 	print("notification read")
		# when the socket connects
		#print(event)

		message_type = event.get('type', None)
		if message_type == "notification_read":
			# Update the notification read status flag in Notification model.
			notification = Notification.object.get(id=notification_id)
			notification.notification_read = True
			notification.save()  #commit to DB
			print("notification read")
            
		front_text = event.get('text', None)
		print(front_text)
		if front_text is not None:
			loaded_data = json.loads(front_text) # gets json data as dictionary
			req = self.scope['user'].username #self.request.user.username (for testing)
			# msg = loaded_data.get('message')
			user = self.scope['user']
			# print('CURRENT USER', user)
			username = 'default'
			# scope = self.scope
			# print(scope)
			other_user = self.scope['url_route']['kwargs']['username']
			if user.is_authenticated():
				username = user.username
			other_user = self.scope['url_route']['kwargs']['username']
			thread_obj = self.thread_obj
			threads_with_unred = await self.get_thread_with_unread(user)
			print('MESSAGE')
			# print(loaded_data.get('message'))
			msg = loaded_data.get('message')
			# print(len(msg))
			if len(msg) != 0: 
				await self.create_chat_message(user, msg) #create message instance AND notifications
				await self.update_notification_status(user, thread_obj) #check notifcations status
				myResponse = {
						'message':msg,
						'username': username,
						'opponent_username': other_user,
						'req': req,
						'threads_by_user': threads_with_unred,
					}
				print(myResponse)
				await self.channel_layer.group_send(
					self.chat_room, #where to send 
					{
					'type':'chat_message',
					'text':json.dumps(myResponse)
					}
					)

	async def chat_message(self, event):
		print('chat_message', event)
		await self.send({
			'type':'websocket.send',
			'text':event['text']
			})
	async def websocket_disconnect(self, event):
		print('WEBSOCKET DISCONNECTS')
		await self.channel_layer.group_discard(
				self.chat_room, 
				self.channel_name
				)
		# print(event)

	@database_sync_to_async
	def get_thread_with_unread(self, user):
		return list(Thread.objects.filter(chatmessage__notification__user=user, chatmessage__notification__read='False').distinct().values_list('id', flat=True))

	@database_sync_to_async
	def get_thread(self, user, other_username, product_slug):
		return Thread.objects.get_or_new(user = user, other_username = other_username, product_slug = product_slug)

	@database_sync_to_async
	def create_chat_message(self, me, msg):
		me = self.scope['user']
		thread_obj = self.thread_obj
		other_user_username = self.scope['url_route']['kwargs']['username']
		other_user = User.objects.filter(username=other_user_username).first()
		msg_created = ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)
		notification_created = Notification.objects.create(message=msg_created, user=other_user, read=False)
		# return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)

	@database_sync_to_async
	def update_notification_status(self, user, thread):
		print('UPDATENOTO')
		print(user)
		unread_notifications = Notification.objects.filter(user=user, read=False).filter(message__thread=thread)
		if unread_notifications:
			# print('HUILALLAA')
			# print('There are some unread notifications')
			# print(unread_notifications)
			# print('yes')  # If am this I am getting this object (thread) and I am this opponent user - Notification.read = True 
			for i in range(len(unread_notifications)):
				unread_notifications[i].read = True
				unread_notifications[i].save()
				# print('Notification read=True')









