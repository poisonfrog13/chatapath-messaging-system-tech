from django.urls import path
from . import views

urlpatterns = [
    path("", views.MessagesList.as_view(), name="messages-list"),
    path("<int:message_pk>", views.MessageDetail.as_view(), name="one-message"),
]
