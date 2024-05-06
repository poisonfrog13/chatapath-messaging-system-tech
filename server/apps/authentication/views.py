from django.shortcuts import get_object_or_404, render

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from server.apps.authentication.serializers import (
    ChatUserSerializer,
    CreateChatUserSerializer,
)
from server.apps.authentication.models import ChatUser
from server.apps.chatapath import serializers


# ------------------------------


@api_view(["POST"])
def signup(request):
    serializer = CreateChatUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = ChatUser.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response(
            {"token": token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    message = {"message": "You successfully have been logged in"}
    user = get_object_or_404(ChatUser, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response(
            {"detail": "Wrong Password"}, status=status.HTTP_400_BAD_REQUEST
        )
    token, created = Token.objects.get_or_create(user=user)
    serializer = ChatUserSerializer(instance=user)
    return Response(
        {
            "token": token.key,
            "user": serializer.data,
            "message": "You successfully have been logged in",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def logout(request):
    message = {"message": "You successfully have been logged out"}
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(message, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("you passed the test for user {}".format(request.user.username))
