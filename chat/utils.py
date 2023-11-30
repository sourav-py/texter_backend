from userAuth.models import Profile
from .models import Participation

def fetchChatRoomName(chatroom,user):
    if chatroom.mode == "GROUP":
        return chatroom.name
    else:
        #For direct mode, fetch the profile picture
        #of the other user present in this chatroom
        try:
            otherParticipation = Participation.objects.filter(chatroom=chatroom).exclude(user=user)[0]
            return otherParticipation.user.username
        except:
            return user.username
        


def fetchChatRoomAvatar(chatroom,user):
    if chatroom.mode == "GROUP":
        return chatroom.avatar
    else:
        #For direct mode, fetch the profile picture
        #of the other user present in this chatroom
        try:
            otherParticipation = Participation.objects.filter(chatroom=chatroom).exclude(user=user)[0]
            return otherParticipation.user.avatar.url
        except:
            user.avatar.url

