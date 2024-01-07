import json
import jwt
from django.utils import timezone

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message, ChatRoom


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        #Fetching user id from ws scope 
        jwtToken = self.scope['cookies'].get('jwt')
        payload = jwt.decode(jwtToken,'secret',algorithms=['HS256'])
        userId = payload['id']

        print("user - ",userId," connected.")

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        userId = text_data_json["userId"]
        messageType = text_data_json["messageType"]

        #Fetching user id from ws scope 
        #jwtToken = self.scope['cookies'].get('jwt')
        #payload = jwt.decode(jwtToken,'secret',algorithms=['HS256'])
        #userId = payload['id']

        if messageType != "typing":
            messageObj = Message.objects.create(sender_id=userId,chatroom_id=int(self.room_name),body=message)
            messageObj.save()

        chatroomObj = ChatRoom.objects.get(id=int(self.room_name))
        chatroomObj.last_updated = timezone.now()
        chatroomObj.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": { "type": messageType, "userId": userId, "body": message}}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))