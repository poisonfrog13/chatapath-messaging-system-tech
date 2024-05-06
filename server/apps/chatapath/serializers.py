from rest_framework import serializers

from server.apps.chatapath.models import Message
from server.apps.authentication.serializers import ChatUserSerializer


class AllMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    sender = ChatUserSerializer()
    recipient = ChatUserSerializer()


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    def validate_sender(self, value):
        """check user is sender"""

        user = self.context.get("user")
        if user != value:
            raise serializers.ValidationError(
                "forbidden, can not send messages as another user"
            )

        return value
