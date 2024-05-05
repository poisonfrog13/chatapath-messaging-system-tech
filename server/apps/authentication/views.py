from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from server.apps.authentication.models import ChatUser
from server.apps.chatapath.models import Message

# Create your views here.


def hello_auth(request):
    return HttpResponse("Hello Auth!")


# to sort messages
