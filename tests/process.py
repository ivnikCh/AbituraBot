from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from random import getrandbits
from user import User
from application import App
from telegram.error import BadRequest
import telegram.ext.filters as filters

Context = ContextTypes(user_data=User)

help_messege = """/help - список команд

/cancel - отменит текущую операцию

/add - подать документы на программу

/show_apps - покажет список всех поданных заявок и их статусы (каждое из заявлений можно будет отозвать /delete) 
"""



async def wrong_cmd(update: Update, context: Context.context) -> int:
    """Send that command is wrong"""
    await update.message.reply_text('Такой команды не существует')
    return ConversationHandler.END

async def help_callback(update: Update, context: Context.context) -> int:
    """Send help messege"""
    await update.message.reply_text(help_messege)
    return ConversationHandler.END

async def cancel_callback(update: Update, context: Context.context) -> int:
    """Cancel operation"""
    context.user_data.app_id = None
    await update.message.reply_text('Операция отменена')
    return ConversationHandler.END



async def all_apps(update: Update, context: Context.context) -> int:
    """Send lists of application"""
    context.user_data.app_id = None
    
    await update.message.reply_text(
        'У вас нет активных заявлений' if len(context.user_data.to_str()) == 0 else context.user_data.to_str()
    )
    return ConversationHandler.END


PASS_ID, URL_DOCS, NAME_PROGRAM = range(3)
stack_in = {}

async def start_input(update: Update, context: Context.context) -> int:
    """Enter passport id"""
    context.user_data.app_id = None
    await update.message.reply_text('Введите код и номер паспорта:')
    return PASS_ID

async def pass_id(update: Update, context: Context.context) -> int:
    """Enter url"""
    stack_in['pass_id'] = update.message.text
    await update.message.reply_text('Введите ссылку на гугл диск с документами:')
    return URL_DOCS

async def url_docs(update: Update, context: Context.context) -> int:
    """Enter name program"""
    stack_in['url_docs'] = update.message.text
    await update.message.reply_text('Введите наззвание образовательной программы:')
    return NAME_PROGRAM

async def add_app(update: Update, context: Context.context) -> int:
    """Add application in data"""
    stack_in['name_program'] = update.message.text
    context.user_data.add_app(stack_in['pass_id'], stack_in['url_docs'], stack_in['name_program'], 'NEW', '')
    await update.message.reply_text('Добавлен')
    return ConversationHandler.END

async def del_app(update: Update, context: Context.context) -> int:
    """Delete application"""
    app_id = context.user_data.app_id
    if app_id is None:
        await update.message.reply_text('Ошибка')
        return ConversationHandler.END
    context.user_data.delete_app(app_id)
    context.user_data.app_id = None
    await update.message.reply_text('Удален')
    return ConversationHandler.END

async def find_app(update: Update, context: Context.context) -> int:
    """Get app"""
    app_id = int(context.matches[0].group(1))
    context.user_data.app_id = app_id
    apps = context.user_data.apps
    await update.message.reply_text(apps[app_id].to_str())
    await update.message.reply_text('Удалить: /delete')
    return ConversationHandler.END

help_handler = CommandHandler(['start', 'help'], help_callback)
cancel_handler = CommandHandler('cancel', cancel_callback)
all_handler = CommandHandler('show_apps', all_apps)
app_handler = MessageHandler(filters.Regex(r'^/(\d+)Application$'), find_app)

init_add_handler = CommandHandler('add', start_input)
pass_add_handler = MessageHandler(filters.TEXT, pass_id)
url_docs_add_handler = MessageHandler(filters.TEXT, url_docs)
name_program_add_handler = MessageHandler(filters.TEXT, add_app)

del_app_handler = CommandHandler('delete', del_app)
wrong_cmd_handler = MessageHandler(None, wrong_cmd)

handlers = [
    help_handler,
    cancel_handler,
    all_handler,
    app_handler,
    init_add_handler,
    del_app_handler,
    wrong_cmd_handler,
]

dialog_handler = ConversationHandler(
    handlers,
    {
        PASS_ID: [help_handler, cancel_handler, pass_add_handler],
        URL_DOCS: [help_handler, cancel_handler, url_docs_add_handler],
        NAME_PROGRAM: [help_handler, cancel_handler, name_program_add_handler],
    },
    handlers,
    name='main_conversation', persistent=True
)
all_handler = [dialog_handler]
