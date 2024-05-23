from telegram.ext import Application, ApplicationBuilder
from pymongo import MongoClient
from process import Context
from router import Router
from gen_token import MY_TOKEN
from process import all_handler
if __name__ == '__main__':
    async def shut(app: Application) -> None:
        mongo_client.close()
    mongo_client = MongoClient()
    persistence = Router(mongo_client.mongo_db)
    app = (ApplicationBuilder()
           .concurrent_updates(False)
           .context_types(Context)
           .persistence(persistence)
           .token(MY_TOKEN)
           .post_shutdown(shut)
           ).build()
    for h in all_handler:
        app.add_handler(h)
    app.run_polling()
