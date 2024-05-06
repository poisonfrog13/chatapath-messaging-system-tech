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
    phone_number = "+44 7468 345579"
    password = factory.Faker("sha256")


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    sender = factory.SubFactory(ChatUserFactory)
    recipient = factory.SubFactory(ChatUserFactory)
    subject = factory.Faker("sentence")
    content = factory.Faker("text")
