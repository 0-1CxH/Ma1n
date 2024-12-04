from flask_login import UserMixin
from .sqlite_utils import sqlite_connect_and_execute

# User class
class User(UserMixin):
    def __init__(self, username, perm_type, resrc_type):
        self.username = username
        self.perm_type = perm_type
        self.resrc_type = resrc_type
    
    def get_id(self):
        return self.username


class UserManager:
    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS user_info (
            username TEXT PRIMARY KEY,
            perm_type INTEGER NOT NULL DEFAULT 0,
            resrc_type INTEGER NOT NULL DEFAULT 0,
            password TEXT NOT NULL
        )
    '''
    insert_user_sql = "INSERT INTO user_info (username, perm_type, resrc_type, password) VALUES (?, ?, ?, ?)"
    authenticate_user_sql = '''
        SELECT password FROM user_info
        WHERE username = ? 
    ''' 
    load_user_sql = '''
        SELECT username, perm_type, resrc_type FROM user_info
        WHERE username = ? 
    ''' 



    user_manager_instance = None

    
    def __init__(self, user_db_path: str) -> None:
        if UserManager.user_manager_instance is not None:
            return
        self.user_db_path = user_db_path
        sqlite_connect_and_execute(self.user_db_path, self.create_table_sql)
        UserManager.user_manager_instance = self


    def add_user(self, user_args: dict) -> bool:
        sqlite_connect_and_execute(
            self.user_db_path, 
            self.insert_user_sql, 
            args=(user_args.get('username'), user_args.get('perm_type', 0), user_args.get('resrc_type', 0), user_args.get('password'))
        )


    def authenticate(self, username: str, password: str):
        row = sqlite_connect_and_execute(
            self.user_db_path, 
            self.authenticate_user_sql,
            args=(username,),
            fetch="one"
        )
        if row:
            password_in_db = row[0]
            if password_in_db == password:
                return username
            else:
                return None
        return None
    
    def load_user(self, username: str) -> User:
        row = sqlite_connect_and_execute(
            self.user_db_path, 
            self.load_user_sql,
            args=(username,),
            fetch="one"
        )
        if row:
            return User(*row)
        return None