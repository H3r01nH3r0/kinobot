from pymongo import MongoClient, errors
from pymongo.cursor import Cursor
from typing import Optional, Union, Dict


class DataBase:
    def __init__(self, db_url: str, db_name: str) -> None:
        try:
            self.client = MongoClient(
                db_url, connect=False,
                serverSelectionTimeoutMS=2000
            )

        except errors.ConnectionFailure:
            exit("Can`t connect to server!")

        self.db = self.client[db_name]
        self._users = self.db.users


    def add_user(self, user_id: int) -> str:
        return self._users.insert_one({"user_id": user_id, "lang": None}).inserted_id

    def get_user(self, user_id: Optional[int]=None) -> Union[Cursor, Dict]:
        if user_id:
            return self._users.find_one({"user_id": user_id})

        return self._users.find({})

    def get_users_count(self) -> int:
        return self._users.count_documents({})

    def edit_user(self, user_id: int, data: dict) -> int:
        return self._users.update_one({"user_id": user_id}, {"$set": data}).modified_count

    def delete_user(self, user_id) -> int:
        result = self._users.delete_one({"user_id": user_id})
        return result.deleted_count

    def close(self) -> None:
        self.client.close()
