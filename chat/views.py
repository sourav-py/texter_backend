# chat/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json

from .models import ChatRoom,Participation
from userAuth.models import Profile

from phonenumber_field.phonenumber import PhoneNumber

from .utils import *

def index(request):
    return render(request, "chat/index.html")

def room(request,room_name):
    return render(request,"chat/room.html",{"room_name": room_name})


"""

::::::PARTICIPATION VIEWS::::::::

"""

#Fetch phone numbers, create a chat room and participation objects
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
                    "chatroomId": chatroom.id,
                    "chatroomName": fetchChatRoomName(chatroom,user),
                    "chatroomPicture": fetchChatRoomAvatar(chatroom,user)
                }
            )

        response = Response()
        #response.data = json.dumps(chatrooms,indent=2)
        response.data = chatrooms

        return response
        
