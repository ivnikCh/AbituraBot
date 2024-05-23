from telegram.ext import BasePersistence
from pymongo.database import Database
from user import User


class Router(BasePersistence):
    """Class for operation with data base"""

    def __init__(self, bd: Database):
        super().__init__()
        self.bd = bd

    async def get_user_data(self) -> dict:
        """Return data for all users"""
        return {
            data["user_id"]: User.from_json(data["user_data"])
            for data in self.bd.data.find()
        }

    async def update_user_data(self, user_id: int, data: User) -> None:
        """Update user by user_id."""
        self.bd.user_data.update_one(
            {"user_id": user_id}, {"$set": {"user_data": data.to_json()}}
        )

    async def drop_user_data(self, user_id: int) -> None:
        """Delete user by user_id"""
        self.bd.user_data.delet_one({"user_id": user_id})

    async def get_conversations(self, name: str) -> dict:
        """Return column info"""
        return {tuple(data["key"]): data["state"] for data in self.bd[name].find()}

    async def update_conversation(self, name: str, key: tuple, new_state: int) -> None:
        """Edit ConversationHandler"""
        self.bd[name].update_one({"key": list(key)}, {"$set": {"state": new_state}})

    async def get_callback_data(self) -> None:
        pass

    async def refresh_user_data(self, user_id: int, user_data: User) -> None:
        pass

    async def update_chat_data(self, chat_id: int, data: dict) -> None:
        pass

    async def refresh_chat_data(self, chat_id: int, chat_data: dict) -> None:
        pass

    async def update_bot_data(self, data: dict) -> None:
        pass

    async def refresh_bot_data(self, bot_data: dict) -> None:
        pass

    async def drop_chat_data(self, chat_id: int) -> None:
        pass

    async def update_callback_data(self, data: dict) -> None:
        pass

    async def flush(self) -> None:
        pass

    async def get_chat_data(self) -> dict:
        return dict()

    async def get_bot_data(self) -> dict:
        return dict()
