from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["sender", "chatroom", "body", "timestamp"]
        depth = 1 