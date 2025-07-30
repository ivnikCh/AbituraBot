import pytest
from application import App
from user import User

@pytest.fixture
def app_data():
    return {
        "pass_id": "123456",
        "url_docs": "http://example.com/docs",
        "name_program": "Example Program",
        "state": "NEW",
        "comment": "No comments"
    }

@pytest.fixture
def user_data(app_data):
    return {
        "app_id": None,
        "apps": [app_data]
    }

@pytest.fixture
def user():
    return User()

def test_to_json(user, app_data):
    user.add_app(**app_data)
    json_data = user.to_json()
    assert json_data["app_id"] is None
    assert len(json_data["apps"]) == 1
    assert json_data["apps"][0]["pass_id"] == app_data["pass_id"]

def test_add_app(user, app_data):
    user.add_app(**app_data)
    assert len(user.apps) == 1
    assert user.apps[0].pass_id == app_data["pass_id"]

def test_delete_app(user, app_data):
    user.add_app(**app_data)
    user.delete_app(0)
    assert user.apps[0].is_delete is True
    assert user.count_apps == -1
