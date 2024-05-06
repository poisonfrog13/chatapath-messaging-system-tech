from rest_framework import serializers

from server.apps.authentication.models import ChatUser
from phonenumber_field.serializerfields import PhoneNumberField


class CreateChatUserSerializer(serializers.ModelSerializer):
    """To deserialize from JSON into ChatUser"""

    class Meta:
        model = ChatUser
        fields = ("username", "email", "password", "phone_number")

    phone_number = PhoneNumberField()


class ChatUserSerializer(serializers.ModelSerializer):
    """To serialize from ChatUser to JSON"""

    class Meta:
        model = ChatUser
        fields = ("id", "username", "phone_number")

    phone_number = PhoneNumberField(required=True)
