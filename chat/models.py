from django.db import models
from userAuth.models import Profile
# Create your models here.

class ChatRoom(models.Model):
    mode = models.CharField(
        max_length = 20,
        choices = (("DIRECT","DIRECT"),("GROUP","GROUP")),
        default = "DIRECT"
    )   

class Participation(models.Model):
    user = models.ManyToManyField(Profile,blank=False)
    chatroom = models.ManyToManyField(ChatRoom,blank=False)

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
    
