from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class SendMessageSer(serializers.Serializer):
    receive_user_id = serializers.IntegerField()
    message = serializers.CharField(max_length=255)


class SendMessageResponse(serializers.Serializer):
    detail = serializers.CharField(max_length=255)
    success = serializers.BooleanField()


class MessagesResponseModel(serializers.Serializer):
    send_user = MessageSerializer(many=True)
    receive_user = MessageSerializer(many=True)
