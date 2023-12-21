# chat/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import json

from .models import ChatRoom,Participation,Message, UnsentMessage
from userAuth.models import Profile

from .serializers import MessageSerializer

from phonenumber_field.phonenumber import PhoneNumber

from .utils import *

def index(request):
    return render(request, "chat/index.html")

def room(request,room_name):
    return render(request,"chat/room.html",{"room_name": room_name})


"""
    API to create a participations for a newly created chatroom
"""
class Participations(APIView):

    permission_classes = [AllowAny]

    def post(self,request):
        phoneNumbers = request.data['phoneNumbers']

        #Create a new chatroom
        chatroomObject = ChatRoom.objects.create(mode="DIRECT")
        chatroomObject.save()

        #Create a participation object for each of the 
        #recieved phone numbers with the newly created
        #chat room.
        for phoneNumber in phoneNumbers:
            profileObject = Profile.objects.get(phone = PhoneNumber.from_string(phoneNumber))
            participationObject = Participation.objects.create(user=profileObject,chatroom = chatroomObject)
            participationObject.save()


        response = Response()
        return response 


"""
API to fetch all the chatrooms that a particular user is a part of
"""
class ChatRooms(APIView):
    permission_classes = [ AllowAny ]
    def post(self,request):
        #Fetch chat rooms that the user is a part of
        
        phoneNumber = PhoneNumber.from_string(request.data['phoneNumber'])
        profileObject = Profile.objects.get(phone=phoneNumber)

        ParticipationSet = Participation.objects.filter(user=profileObject)

        chatrooms = []

        for participation in ParticipationSet:
            chatroom = participation.chatroom
            user = participation.user 

            chatrooms.append(
                {
                    "id": chatroom.id,
                    "name": fetchChatRoomName(chatroom,user),
                    "avatar": fetchChatRoomAvatar(chatroom,user),
                    "last_updated": chatroom.last_updated
                }
            )
        chatrooms = sorted(chatrooms,key = lambda x: x['last_updated'],reverse=True)

        response = Response()
        #response.data = json.dumps(chatrooms,indent=2)
        response.data = JSONRenderer().render(chatrooms)

        print(response.data)

        return response
        


"""
    API to fetch messages sent to a particular chatroom
"""
class Messages(APIView):
    permission_classes = [AllowAny]

    def post(self,request):

        #Pull chatroom id from request data
        #and fetch messages sent to that chatroom

        chatRoomId = request.data['chatRoomId']
        chatRoom = ChatRoom.objects.get(id=chatRoomId)

        messages = Message.objects.filter(chatroom = chatRoom)

        responseData = []

        for message in messages:
            serializedMessage = MessageSerializer(message)
            responseData.append(serializedMessage.data)


        response = Response()
        response.data = responseData
        return response



"""
    API to confirm the message reception for a particular user and message
"""
class MessageDelivery(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        messageId = request.data['messageId']
        userId = request.data['userId']

        userObj = Profile.objects.get(id=userId)
        messageObj = Message.objects.get(id=messageId)

        #Fetch the unsent message instance corresponding the recieved userId and messageId and delete the instance.
        unsentMessageObj = UnsentMessage.objects.get(message=messageObj,user=userObj)
        if unsentMessageObj:
            unsentMessageObj.delete()

        response = Response()
        return response

