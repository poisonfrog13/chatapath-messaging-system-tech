from django.urls import path
from . import views

MESSAGES_LIST = "messages-list"
ONE_MESSAGE = "message-detail"

urlpatterns = [
    path("", views.MessagesList.as_view(), name=MESSAGES_LIST),
    path("<int:message_pk>", views.MessageDetail.as_view(), name=ONE_MESSAGE),
]
