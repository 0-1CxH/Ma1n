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


@dataclass
class NodeContent:
    content_type: str # M[material], D[dialog]
    io_type: str # I[input], O[output]
    title: str
    note: str
    level: int
    cap_img_path: str = None





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
        SELECT owner_username, conversation_folder 
        FROM session_info 
        WHERE session_id = ?
    '''

    delete_session_sql = '''
        DELETE FROM session_info
        WHERE session_id = ? 
    '''

    abst_filename = "abst.json"
    nodes_filename = "nodes.json"
    input_material_folder_name = "input_material/"
    output_material_folder_name = "output_material/"

    def __init__(self, session_db_path: str, conversation_store_root: str) -> None:
        if ConversationManager.conversation_manager_instance is not None:
            return
        self.session_db_path = session_db_path
        self.conversation_store_root = conversation_store_root
        sqlite_connect_and_execute(self.session_db_path, self.create_table_sql)
        ConversationManager.user_manager_instance = self
    
    def add_conversation_info(self, session_id, owner_username, all_submitted_content):
        conversation_folder = os.path.join(self.conversation_store_root, owner_username, session_id)
        # build folder and insert to db 
        sqlite_connect_and_execute(
            self.session_db_path,
            self.insert_session_sql,
            args=(session_id, owner_username, conversation_folder)
        )
        os.makedirs(conversation_folder)
        
        # save abst file to folder
        abst_file_path = os.path.join(conversation_folder, self.abst_filename)
        title = all_submitted_content["user_input"][:50]
        if len(title) == 0:
            title = "(No Title for Now, will Generate Soon)"
        note = f'{all_submitted_content["selected_process_function"]} of {len(all_submitted_content["uploaded_files"])} file(s) and {len(all_submitted_content["entered_links"])} link(s)'
        conv_abst = ConversationAbstract(
            title=title,
            ctime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            abst="(No Abstract for Now, will Generate Soon)",
            note=note,
        )
        conv_abst.to_file(abst_file_path)

        # process the files and links
        
        # save nodes file to folder
        nodes_file_path = os.path.join(conversation_folder, self.nodes_filename)
        with open(nodes_file_path, "w") as f:
            f.write(json.dumps({}, ensure_ascii=False, indent=4))
        

    
    def get_conversation_abstract(self, conversation_folder):
        # get abst from folder
        abst_file_path = os.path.join(conversation_folder, self.abst_filename)
        return ConversationAbstract.from_file(abst_file_path)
    

    def get_session_info_by_id(self, session_id, username):
        owner, conv_folder = sqlite_connect_and_execute(
            self.session_db_path, 
            self.query_session_by_id_sql,
            args=(session_id,),
            fetch="one"
        )
        if owner == username:
            conv_nodes_file = os.path.join(conv_folder, self.nodes_filename)
            try:
                with open(conv_nodes_file) as f:
                    conv_nodes_file_content = json.loads(f.read())
                    return {
                        "code": 0, 
                        "conv_folder": conv_folder, 
                        "conv_nodes_file_content": conv_nodes_file_content
                    }
            except Exception as e:
                return {"code": -2, "reason": e.__str__()}

        else:
            return {"code": -1, "reason": "No Permission."}


    
    def delete_conversation_info(self, session_id, username):
        # delete folder (including abst, inpt, otpt and everything) and remove from db
        owner, conv_folder = sqlite_connect_and_execute(
            self.session_db_path, 
            self.query_session_by_id_sql,
            args=(session_id,),
            fetch="one"
        )
        if owner == username:
            sqlite_connect_and_execute(
                self.session_db_path,
                self.delete_session_sql,
                args=(session_id,)
            )
            try:
                shutil.rmtree(conv_folder)
                return {"code": 0}
            except:
                return {"code": ret_code, "reason": "File Already Deleted."}
        else:
            return {"code": -1, "reason": "No Permission."}

    
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
        
        
