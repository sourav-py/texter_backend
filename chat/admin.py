from django.contrib import admin
from .models import ChatRoom, Participation, Message
# Register your models here.

admin.site.register(ChatRoom)
admin.site.register(Participation)
admin.site.register(Message)
