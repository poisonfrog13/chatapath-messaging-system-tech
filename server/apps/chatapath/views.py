from email import message
from django.db.models import Q
from django.shortcuts import get_object_or_404


from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from server.apps.authentication.models import ChatUser
from server.apps.authentication.serializers import ChatUserSerializer
from server.apps.chatapath.models import Message
from server.apps.chatapath.serializers import (
    AllMessagesSerializer,
    CreateMessageSerializer,
)

# -------------------------------------------------


class MessagesList(APIView):
    # class MessagesList(generics.ListAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # queryset = Message.objects.all()
    # serializer_class = AllMessagesSerializer
    # filterset_fields = ["is_unread", "recipient", "sender"]

    def get(self, request, format=None):
        """Retrieve all messages where the user is the sender or the recipient;
        Fetch unread messages for the user as recipient -->
        Add '?is_unread=true' in browser for unread messages"""

        # Query parameters
        only__unread = self.request.query_params.get("is_unread") == "true"
        only__seen = self.request.query_params.get("is_unread") == "false"
        only__incoming = self.request.query_params.get("transaction") == "incoming"
        only__outgoing = self.request.query_params.get("transaction") == "outgoing"

        all_messages = Message.objects.filter(
            (Q(sender=request.user.id) | Q(recipient=request.user.id))
        )

        serializer = AllMessagesSerializer(
            all_messages, many=True, context={"user": request.user}
        )

        if only__incoming:
            serializer = serializer.incoming

        elif only__outgoing:
            serializer = serializer.outgoing

        elif only__unread:
            serializer = serializer.is_unread

        elif only__seen:
            serializer = serializer.seen

        else:
            serializer = serializer.data

        return Response(
            serializer,
            status=(status.HTTP_200_OK if all_messages else status.HTTP_204_NO_CONTENT),
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
