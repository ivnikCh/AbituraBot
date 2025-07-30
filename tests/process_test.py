import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from process import (
    wrong_cmd,
    help_callback,
    cancel_callback,
    all_apps,
    start_input,
    pass_id,
    url_docs,
    add_app,
    del_app,
    find_app,
    help_messege,
    PASS_ID,
    URL_DOCS,
    NAME_PROGRAM,
    stack_in
)
from user import User
@pytest_asyncio.fixture
def context():
    return ContextTypes(user_data=User)

@pytest_asyncio.fixture
def update():
    return AsyncMock(Update)

@pytest.mark.asyncio
async def test_wrong_cmd(update, context):
    update.message.reply_text = AsyncMock()
    result = await wrong_cmd(update, context)
    update.message.reply_text.assert_called_once_with('Такой команды не существует')
    assert result == ConversationHandler.END

@pytest.mark.asyncio
async def test_help_callback(update, context):
    update.message.reply_text = AsyncMock()
    result = await help_callback(update, context)
    update.message.reply_text.assert_called_once_with(help_messege)
    assert result == ConversationHandler.END

@pytest.mark.asyncio
async def test_cancel_callback(update, context):
    update.message.reply_text = AsyncMock()
    result = await cancel_callback(update, context)
    update.message.reply_text.assert_called_once_with('Операция отменена')
    assert context.user_data.app_id is None
    assert result == ConversationHandler.END

@pytest.mark.asyncio
async def test_all_apps(update, context):
    update.message.reply_text = AsyncMock()
    context.user_data.to_str = MagicMock(return_value='Test Application')
    result = await all_apps(update, context)
    update.message.reply_text.assert_called_once_with('Test Application')
    assert context.user_data.app_id is None
    assert result == ConversationHandler.END

@pytest.mark.asyncio
async def test_start_input(update, context):
    update.message.reply_text = AsyncMock()
    result = await start_input(update, context)
    update.message.reply_text.assert_called_once_with('Введите код и номер паспорта:')
    assert context.user_data.app_id is None
    assert result == PASS_ID

@pytest.mark.asyncio
async def test_pass_id(update, context):
    update.message.reply_text = AsyncMock()
    update.message.text = '123456'
    result = await pass_id(update, context)
    assert stack_in['pass_id'] == '123456'
    update.message.reply_text.assert_called_once_with('Введите ссылку на гугл диск с документами:')
    assert result == URL_DOCS

@pytest.mark.asyncio
async def test_url_docs(update, context):
    update.message.reply_text = AsyncMock()
    update.message.text = 'http://example.com'
    result = await url_docs(update, context)
    assert stack_in['url_docs'] == 'http://example.com'
    update.message.reply_text.assert_called_once_with('Введите наззвание образовательной программы:')
    assert result == NAME_PROGRAM
