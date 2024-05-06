from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from server.apps.chatapath.models import Message
from server.apps.chatapath.serializers import (
    AllMessagesSerializer,
    CreateMessageSerializer,
)

# -------------------------------------------------


class MessagesList(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """Retrieve all messages where the user is the sender or the recipient;
        Fetch unread messages for the user as recipient -->
        Add '?is_unread=true' in browser for unread messages"""

        unread_messages_only = self.request.query_params.get("is_unread") == "true"

        query = (
            (Q(recipient=request.user.id) & Q(is_unread=True))
            if unread_messages_only
            else (Q(sender=request.user.id) | Q(recipient=request.user.id))
        )

        all_messages = Message.objects.filter(query)
        serializer = AllMessagesSerializer(all_messages, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK if all_messages else status.HTTP_204_NO_CONTENT,
        )

    def post(self, request, format=None):
        serializer = CreateMessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageDetail(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, message_pk, format=None):
        message = get_object_or_404(Message, pk=message_pk)
        serializer = AllMessagesSerializer(message)
        allowed = message.sender == request.user or message.recipient == request.user

        if allowed:
            message.is_unread = False
            message.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, message_pk, format=None):
        message = get_object_or_404(Message, pk=message_pk)
        allowed = message.sender == request.user or message.recipient == request.user

        if allowed:
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
