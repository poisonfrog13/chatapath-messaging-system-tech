from more_itertools import all_equal
from rest_framework import serializers

from server.apps.chatapath.models import Message
from server.apps.authentication.serializers import ChatUserSerializer


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class AllMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    sender = ChatUserSerializer()
    recipient = ChatUserSerializer()

    def to_representation(self, instance):
        user = self.context.get("user")
        data = super().to_representation(instance)
        print(instance)
        data["transaction"] = "incoming" if user == instance.recipient else "outgoing"
        data["is_unread"] = True if instance.is_unread == True else False
        return data
