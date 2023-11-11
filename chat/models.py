from django.db import models
from userAuth.models import Profile
# Create your models here.

class ChatRoom(models.Model):
    mode = models.CharField(
        max_length = 20,
        choices = (("DIRECT","DIRECT"),("GROUP","GROUP")),
        default = "DIRECT"
    )   
    name = models.CharField(max_length=100,blank=True,null=True)
    avatar = models.ImageField(upload_to='avatars/',null=True, blank=True)


class Participation(models.Model):
    user = models.ForeignKey(Profile,models.CASCADE,blank=False)
    chatroom = models.ForeignKey(ChatRoom,models.CASCADE,blank=False)

class Message(models.Model):
    sender = models.ForeignKey(
        Profile,
        models.SET_NULL,#incase the Profile gets deleted
        null=True,
    )
    chatroom = models.ForeignKey(
        ChatRoom,
        models.SET_NULL, #incase the chatroom gets deleted
        null=True               
    )
    body = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

class UnsentMessage(models.Model):
    user = models.ForeignKey(Profile,models.CASCADE,blank=False)
    message = models.ForeignKey(Message,models.CASCADE,blank=False)


    
