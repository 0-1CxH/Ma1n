import os
import json
import shutil
import datetime
from dataclasses import dataclass
from .sqlite_utils import sqlite_connect_and_execute


@dataclass
class ConversationAbstract:
    title: str
    ctime: str
    abst: str
    note: str

    def to_file(self, abst_file):
        with open(abst_file, "w") as f:
            json.dump(self.__dict__, f, ensure_ascii=False)
    
    @classmethod
    def from_file(cls, abst_file):
        if not os.path.exists(abst_file):
            return cls(
                title = "Infomation Not Found",
                ctime = "",
                abst = f"The abstract file at {abst_file} is missing.",
                note = ""
            )
        with open(abst_file) as f:
            return cls(**json.load(f))




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
            conversation_folder TEXT NOT NULL
        )
    '''

    query_session_sql =  '''
        SELECT session_id, conversation_folder 
        FROM session_info 
        WHERE owner_username = ?
    '''

    insert_session_sql = '''
        INSERT INTO session_info (session_id, owner_username, conversation_folder) VALUES (?, ?, ?)
    '''

    query_session_by_id_sql = '''
        SELECT conversation_folder 
        FROM session_info 
        WHERE session_id = ?
    '''

    delete_session_sql = '''
        DELETE FROM session_info
        WHERE session_id = ? 
    '''

    abst_filename = "abst.json"

    def __init__(self, session_db_path: str, conversation_store_root: str) -> None:
        if ConversationManager.conversation_manager_instance is not None:
            return
        self.session_db_path = session_db_path
        self.conversation_store_root = conversation_store_root
        sqlite_connect_and_execute(self.session_db_path, self.create_table_sql)
        ConversationManager.user_manager_instance = self
    

    
    def add_conversation_info(self, session_id, owner_username, conversation_folder):
        # build folder and insert to db 
        sqlite_connect_and_execute(
            self.session_db_path,
            self.insert_session_sql,
            args=(session_id, owner_username, conversation_folder)
        )
        os.makedirs(conversation_folder)
    
    def add_conversation_abstract(self, conversation_folder, title, note):
        # save abst to folder
        abst_file_path = os.path.join(conversation_folder, self.abst_filename)
        if len(title) == 0:
            title = "(No Title for Now, will Generate Soon)"
        conv_abst = ConversationAbstract(
            title=title,
            ctime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            abst="(No Abstract for Now, will Generate Soon)",
            note=note,
        )
        conv_abst.to_file(abst_file_path)
    
    def get_conversation_abstract(self, conversation_folder):
        # get abst from folder
        abst_file_path = os.path.join(conversation_folder, self.abst_filename)
        return ConversationAbstract.from_file(abst_file_path)
        

    
    def delete_conversation_info(self, session_id):
        # delete folder (including abst, inpt, otpt and everything) and remove from db
        row = sqlite_connect_and_execute(
            self.session_db_path, 
            self.query_session_by_id_sql,
            args=(session_id,),
            fetch="one"
        )
        sqlite_connect_and_execute(
            self.session_db_path,
            self.delete_session_sql,
            args=(session_id,)
        )
        shutil.rmtree(row[0])

    
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
                session_id, conversation_folder = row
                conv_abst = self.get_conversation_abstract(conversation_folder)
                all_session_info.append(
                    SessionInfo(conv_abst, session_id)
                )
            all_session_info.sort(key=lambda session: session.conv_abst.ctime, reverse=True)
            return all_session_info

        else:
            return []
        
        
