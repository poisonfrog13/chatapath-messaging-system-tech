# def test_user_phonenumber_cannot_update(db, chat_user_factory): ...
# def test_message_date_cannot_update(db, message_factory): ...
#
import pytest

from rest_framework.test import APIClient

client = APIClient()
