import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage


class ChatConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		# when the socket connects
		print('connected', event)
		other_user = self.scope['url_route']['kwargs']['username'] #get that username from url kwargs, kwargs coming from routing.py urls
		me = self.scope['user'] # takes user this.username gives username
		thread_obj = await self.get_thread(me, other_user)
		print(me, thread_obj.id)
		self.thread_obj = thread_obj
		chat_room = f'thread_{thread_obj.id}'
		self.chat_room = chat_room
		await self.channel_layer.group_add(
			chat_room, #where to send
			self.channel_name #default attr from channels
			)
		await self.send({
			'type':'websocket.accept'
			})

	async def websocket_receive(self, event):
		# when the socket connects
		print(event)
		front_text = event.get('text', None)
		if front_text is not None:
			loaded_data = json.loads(front_text) # gets json data as dictionary
			msg = loaded_data.get('message')
			user = self.scope['user']
			username = 'default'
			req = self.scope['user'].username
			other_user = self.scope['url_route']['kwargs']['username']
			if user.is_authenticated():
				username = user.username
			myResponse = {
					'message':msg,
					'username': username,
					'opponent_username': other_user,
					'req': req,
				}
			await self.create_chat_message(user, msg)
			await self.channel_layer.group_send(
				self.chat_room, #where to send 
				{
				'type':'chat_message',
				'text':json.dumps(myResponse)
				}
				)

	async def chat_message(self, event):
		print('message', event)
		await self.send({
			'type':'websocket.send',
			'text':event['text']
			})
	async def websocket_disconnect(self, event):
		await self.channel_layer.group_discard(
				self.room_group_name, 
				self.channel_name
				)
		print(event)

	@database_sync_to_async
	def get_thread(self, user, other_username):
		return Thread.objects.get_or_new(user, other_username)[0]

	@database_sync_to_async
	def create_chat_message(self, me, msg):
		thread_obj = self.thread_obj
		return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)








