from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import Message
from chat.schemas import send_message_schema, get_message_schema
from chat.serializers import SendMessageSer, MessagesResponseModel
from utils.pagination import paginate


@send_message_schema
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request):
    serializer = SendMessageSer(data=request.data)
    if serializer.is_valid():
        receive_user = User.objects.filter(id=serializer.data['receive_user_id']).first()
        if not receive_user:
            return Response({'detail': 'Received user not found!',
                             'success': False})
        message = Message.objects.create(
            send_user_id=request.user,
            receive_user_id=receive_user,
            message=serializer.data['message']
        )
        message.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "chat_group",
            {
                "type": "add_new_message",
                "receive_user": receive_user
            },
        )
        return Response({'detail': 'Send message successfully!',
                         'success': True})
    return Response({'detail': 'Error!',
                     'success': False})


@get_message_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request):
    messages = Message.objects
    data = {
        'send_user': messages.filter(send_user_id=request.user).all(),
        'receive_user': messages.filter(receive_user_id=request.user).all()
    }
    serializer = MessagesResponseModel(data)
    return Response(serializer.data, status=200)
