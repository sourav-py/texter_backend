from userAuth.models import Profile
from rest_framework import renderers
from userAuth.serializers import ProfileSerializer
from .models import Participation

def fetchChatRoomName(chatroom,user):
    if chatroom.mode == "GROUP":
        return chatroom.name
    else:
        #For direct mode, fetch the profile picture
        #of the other user present in this chatroom
        try:
            otherParticipation = Participation.objects.filter(chatroom=chatroom).exclude(user=user)[0]
            if otherParticipation.user.name:
                return otherParticipation.user.name
            else:
                return str(otherParticipation.user.phone)
        except:
            if user.name:
                return user.name
            else:
                return str(user.phone)
        


def fetchChatRoomAvatar(chatroom,user):
    if chatroom.mode == "GROUP":
        return chatroom.avatar
    else:
        #For direct mode, fetch the profile picture
        #of the other user present in this chatroom
        try:
            otherParticipation = Participation.objects.filter(chatroom=chatroom).exclude(user=user)[0]
            if otherParticipation.user.avatar:
                return otherParticipation.user.avatar.url
            else:
                return None
        except:
            if user.avatar:
                user.avatar.url
            else:
                return None
