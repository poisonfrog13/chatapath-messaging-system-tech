import pytest

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from tests import factories
from server.apps.chatapath.models import Message
from server.apps.chatapath.urls import MESSAGES_LIST, ONE_MESSAGE

# ----------------- API's


def auth_token(user):
    """To call this function every time, when a token is needed
    To parse a fixture simulated_profile as an argument"""

    token, _ = Token.objects.update_or_create(user=user)
    return {"Authorization": f"Token {token.key}"}


def test_url_non_auth(db, client, user_fixture):
    # Given
    user = user_fixture

    # When + Then
    assert client.get("/chat/").status_code == 403


def test_view__message_list(db, client, user_fixture):
    # Given
    user = user_fixture
    messages = factories.MessageFactory.create_batch(size=10, sender=user)
    messages += factories.MessageFactory.create_batch(size=10, recipient=user)

    # When
    response = client.get(reverse(MESSAGES_LIST), headers=auth_token(user))

    # Then
    assert response.status_code == 200


def test_view__message_list_create(db, client, user_fixture, message_fixture):
    # Given
    user = user_fixture
    recipient = user_fixture
    messages = Message.objects.all()
    init_message_count = messages.count()

    expected_message_count = init_message_count + 1

    new_message = {
        "sender": user.pk,
        "recipient": recipient.pk,
        "subject": "message for test",
        "content": "random content",
    }

    invalid_new_message = {
        "sender": user.pk,
        "recipient": recipient,
        "subject": "klklk",
        "content": 1234,
    }
    # When
    response = client.post(
        reverse(MESSAGES_LIST), data=new_message, headers=auth_token(user)
    )
    invalid_response = client.post(
        reverse(MESSAGES_LIST), data=invalid_new_message, headers=auth_token(user)
    )
    found_messages_count = messages.count()

    # Then
    assert response.status_code == 201, response.content
    assert invalid_response.status_code == 400, response.content
    assert expected_message_count == found_messages_count


def test_view__message_detail(db, client, user_fixture):
    # Given
    user = user_fixture
    messages = factories.MessageFactory.create_batch(size=10, sender=user)
    message_1 = Message.objects.first()
    message_pk = {"message_pk": message_1.pk}
    message_pk_404 = {"message_pk": 2000}

    # When
    response = client.get(
        reverse(ONE_MESSAGE, kwargs=message_pk), headers=auth_token(user)
    )
    response_404 = client.get(
        reverse(ONE_MESSAGE, kwargs=message_pk_404), headers=auth_token(user)
    )
    # Then
    assert response.status_code == 200
    assert response_404.status_code == 404


def test_view__message_detail_delete(db, client, user_fixture):
    # Given
    user = user_fixture
    messages = factories.MessageFactory.create_batch(size=10, sender=user)
    all_messages = Message.objects.all()
    message_to_delete = Message.objects.first()
    message_to_delete__pk = {"message_pk": message_to_delete.pk}
    init_message_count = all_messages.count()

    expected_message_count = init_message_count - 1

    # When
    response = client.delete(
        reverse(ONE_MESSAGE, kwargs=message_to_delete__pk), headers=auth_token(user)
    )
    found_messages_count = all_messages.count()

    # Then
    assert response.status_code == 204, response.content
    assert expected_message_count == found_messages_count
