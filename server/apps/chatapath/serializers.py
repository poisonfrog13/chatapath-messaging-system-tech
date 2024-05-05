from rest_framework import serializers

from server.apps.chatapath.models import Message
from server.apps.authentication.serializers import ChatUserSerializer


class AllMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    sender = ChatUserSerializer()
    recipient = ChatUserSerializer()


# - We can store external informatkion in the serializer using the context kwarg
# -
