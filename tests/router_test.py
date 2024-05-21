import pytest
from asynctest import CoroutineMock, patch
from pymongo import MongoClient
import mongomock
from user import User
from router import Router

@pytest.fixture
def mock_db():
    client = mongomock.MongoClient()
    db = client['test_db']
    return db

@pytest.fixture
def router(mock_db):
    return Router(mock_db)

@pytest.fixture
def user_data():
    return {
        "user_id": 1,
        "user_data": {
            "name": "Test User",
            "age": 30
        }
    }

@pytest.fixture
def user(user_data):
    return User.from_json(user_data['user_data'])

@pytest.mark.asyncio
async def test_get_conversations(router, mock_db):
    mock_db.conversations.insert_one({"key": [1, 2], "state": "active"})
    result = await router.get_conversations("conversations")
    assert (1, 2) in result
    assert result[(1, 2)] == "active"

@pytest.mark.asyncio
async def test_update_conversation(router, mock_db):
    mock_db.conversations.insert_one({"key": [1, 2], "state": "inactive"})
    await router.update_conversation("conversations", (1, 2), "active")
    result = mock_db.conversations.find_one({"key": [1, 2]})
    assert result is not None
    assert result["state"] == "active"

