# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    #path("", views.index, name="index"),
    #path("<str:room_name>/",views.room,name="room"),
    path("participation/",views.Participations.as_view(),name="Participations"),
    path("chatrooms/",views.ChatRooms.as_view(),name="ChatRooms"),
    path("messages/",views.Messages.as_view(),name="Messages"),
]