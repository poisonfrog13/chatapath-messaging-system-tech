import pytest

from pytest_factoryboy import register

from server.apps.authentication.models import ChatUser
from server.apps.chatapath.models import Message
from tests.factories import ChatUserFactory, MessageFactory

# ------------------------------

register(ChatUserFactory)
register(MessageFactory)

# ------------------------------ FOR CHATAPATH & AUTHENTICATION


@pytest.fixture
def user_fixture(db, chat_user_factory):
    user = chat_user_factory.create()
    # print(user.username)
    return user


@pytest.fixture
def message_fixture(db, message_factory):
    message = message_factory.create()
    print(message.subject)
    return message


@pytest.fixture
def simulated_profile_fixture(db, chat_user_factory, message_factory):

    def create_profile(amount_messages=5):
        user_sender = chat_user_factory.create()
        user_recipient = chat_user_factory.create()
        messages = message_factory.create_batch(
            size=amount_messages, user=user_sender, user_recipient=user_recipient
        )

        return user_sender

    return create_profile
