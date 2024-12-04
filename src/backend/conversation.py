from dataclasses import dataclass
from .sqlite_utils import sqlite_connect_and_execute


@dataclass
class ConversationAbstract:
    title: str
    dtime: str
    abst: str
    note: str

@dataclass
class SessionInfo:
    conv_abst: ConversationAbstract
    session_id: str

class ConversationManager:
    conversation_manager_instance = None

    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS session_info (
            session_id TEXT PRIMARY KEY,
            owner_username TEXT NOT NULL,
            file_path TEXT NOT NULL
        )
    '''

    query_session_sql =  '''
        SELECT session_id, file_path 
        FROM session_info 
        WHERE owner_username = ?
    '''

    insert_session_sql = '''
        INSERT INTO session_info (session_id, owner_username, file_path) VALUES (?, ?, ?)
    '''

    def __init__(self, session_db_path: str, conversation_store_root: str) -> None:
        if ConversationManager.conversation_manager_instance is not None:
            return
        self.session_db_path = session_db_path
        self.conversation_store_root = conversation_store_root
        sqlite_connect_and_execute(self.session_db_path, self.create_table_sql)
        ConversationManager.user_manager_instance = self
    
    def read_conversation_file(self, conv_file_path):
        import random
        return ConversationAbstract(**{
            "title": "test",
            "abst": "x" * random.randint(50, 1600),
            "dtime": "10292-01923",
            "note": "cccc",
        })
    
    def add_conversation_info(self, session_id, owner_username, file_path):
        sqlite_connect_and_execute(
            self.session_db_path,
            self.insert_session_sql,
            args=(session_id, owner_username, file_path)
        )
    
    def get_conversations_by_username(self, username):
        rows = sqlite_connect_and_execute(
            self.session_db_path, 
            self.query_session_sql,
            args=(username,),
            fetch="all"
        )
        if rows:
            all_session_info = []
            for row in rows:
                session_id, file_path = row
                conv_abst = self.read_conversation_file(file_path)
                all_session_info.append(
                    SessionInfo(conv_abst, session_id)
                )
            return all_session_info

        else:
            return []
        
        
