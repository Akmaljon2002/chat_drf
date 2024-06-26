from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from asgiref.sync import sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Message
from chat.serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Chat uchun
    """

    async def connect(self):
        token = self.scope.get("query_string").decode("utf-8")
        if token.startswith("token="):
            token = token.replace("token=", "")
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                self.scope["user_id"] = user_id
            except Exception as e:
                await self.close()

        await self.accept()
        await self.channel_layer.group_add("chat_group", self.channel_name)
        # await self.get_initial_message_list()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat_group", self.channel_name)

    async def send_initial_message_list(self, receive_user):
        user_id = self.scope['user_id']
        user = await self.get_user_by_id(user_id)
        if user_id == receive_user.id:
            message_list = await self.get_message_new(user)
            await self.send(text_data=json.dumps(message_list))

    async def get_initial_message_list(self):
        user_id = self.scope['user_id']
        user = await self.get_user_by_id(user_id)
        message_list = await self.get_message_list(user)
        await self.send(text_data=json.dumps(message_list))

    async def add_new_message(self, event):
        receive_user = event['receive_user']
        await self.send_initial_message_list(receive_user)

    @sync_to_async
    def get_message_list(self, user):
        loc_objects = Message.objects.filter(receive_user_id=user.id).all().order_by('datetime')
        serializer = MessageSerializer(loc_objects, many=True)
        return serializer.data

    @sync_to_async
    def get_message_new(self, user):
        loc_objects = Message.objects.filter(receive_user_id=user.id).last()
        serializer = MessageSerializer(loc_objects)
        return serializer.data

    @sync_to_async
    def get_user_by_id(self, user_id):
        return User.objects.filter(id=user_id).first()
