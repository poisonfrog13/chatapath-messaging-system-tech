import pytest

from server.apps.authentication.models import ChatUser
from server.apps.chatapath.models import Message


# ------------------- CREATE


def test_new_user(db, chat_user_factory):
    # Given
    init_count = ChatUser.objects.all().count()

    expected_count = init_count + 1

    # When
    user = chat_user_factory.create()
    found_count = ChatUser.objects.all().count()

    # Then
    assert expected_count == found_count


def test_new_message(db, message_factory):
    # Given
    init_count = Message.objects.all().count()

    expected_count = init_count + 1

    # When
    user = message_factory.create()
    found_count = Message.objects.all().count()

    # Then
    assert expected_count == found_count


# ------------------- UPDATE


def test_user_name_update(db, chat_user_factory):
    # Given
    user = chat_user_factory.create()
    init_name = user.username

    # When
    user.username = "NEWNAME"
    user.save()

    updated_user = ChatUser.objects.get(pk=user.pk)

    new_name = updated_user.username

    # Then
    assert new_name != init_name


def test_message_content_update(db, message_factory):
    # Given
    message = message_factory.create()
    init_content = message.content

    # When
    message.content = "It's a new content for an old message"
    message.save()

    updated_message = Message.objects.get(pk=message.pk)

    new_content = updated_message.content

    # Then
    assert new_content != init_content


# ------------------- DELETE


def test_delete_user(user_fixture):
    # Given
    init_count = ChatUser.objects.all().count()

    expected_count = init_count - 1

    # When
    user_fixture.delete()
    found_count = ChatUser.objects.all().count()

    # Then
    assert found_count == expected_count


def test_delete_message(message_fixture):
    # Given
    init_count = Message.objects.all().count()

    expected_count = init_count - 1

    # When
    message_fixture.delete()
    found_count = Message.objects.all().count()

    # Then
    assert found_count == expected_count


def test_user_message_delete(db, user_fixture, message_factory):
    # Given
    message = message_factory.create(sender=user_fixture)
    message_table = Message.objects.filter(pk=message.pk)
    init_table = message_table.exists()

    # When
    ChatUser.objects.all().delete()
    message_table = Message.objects.filter(pk=message.pk)
    found_table = message_table.exists()

    # Then
    assert found_table != init_table
