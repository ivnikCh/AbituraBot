import pytest
from application import App  

@pytest.fixture
def app_data():
    return {
        "pass_id": "123456",
        "url_docs": "http://example.com/docs",
        "name_program": "Example Program",
        "state": "NEW",
        "comment": "No comments",
        "is_delete": False
    }

@pytest.fixture
def app_instance(app_data):
    return App(**app_data)

def test_from_json(app_data):
    app = App.from_json(app_data)
    assert app.pass_id == app_data["pass_id"]
    assert app.url_docs == app_data["url_docs"]
    assert app.name_program == app_data["name_program"]
    assert app.state == app_data["state"]
    assert app.comment == app_data["comment"]
    assert app.is_delete == app_data["is_delete"]

def test_to_json(app_instance, app_data):
    json_data = app_instance.to_json()
    assert json_data == app_data

def test_to_str(app_instance):
    result_str = app_instance.to_str()
    expected_str = (
        "url for docs "
        + app_instance.url_docs
        + "\n name program - "
        + app_instance.name_program
        + "\n state: "
        + app_instance.state
        + "\n"
        + app_instance.comment
    )
    assert result_str == expected_str

