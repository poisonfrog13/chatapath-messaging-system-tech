import factory
from faker import Faker

from server.apps.authentication.models import ChatUser
from server.apps.chatapath.models import Message


# -------------------------------

fake = Faker()


# -------------------------------
class ChatUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatUser

    username = factory.Faker("name")
    email = factory.Faker("ascii_email")
    phone_number = factory.Faker("msisdn")
    password = "password"


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    sender = factory.SubFactory(ChatUserFactory)
    recipient = factory.SubFactory(ChatUserFactory)
    subject = factory.Faker("sentence")
    content = factory.Faker("text")
