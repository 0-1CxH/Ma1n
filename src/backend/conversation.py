import os
import json
import shutil
import uuid
import wget
import datetime
import requests
from dataclasses import dataclass
from typing import List
from flask_socketio import emit
from .sqlite_utils import sqlite_connect_and_execute
from .defines import ConversationAbstract, ContentNode, ContentEdge, ConversationNodes
from ..intelligence.execute import IntelligenceManger


@dataclass
class SessionInfo:
    conv_abst: ConversationAbstract
    session_id: str
    owner: str




class ConversationFolderStructure:
    abst_filename = "abst.json"
    nodes_filename = "nodes.json"
    input_material_folder_name = "input_material"
    output_material_folder_name = "output_material"

    @classmethod
    def get_conv_abst_obj(cls, conv_folder):
        abst_file_path = os.path.join(conv_folder, cls.abst_filename)
        return ConversationAbstract.from_file(abst_file_path)
    
    @classmethod
    def put_conv_abst_obj(cls, conv_folder, conv_abst_obj):
        abst_file_path = os.path.join(conv_folder, cls.abst_filename)
        conv_abst_obj.to_file(abst_file_path)
    
    @classmethod
    def get_conv_nodes_obj(cls, conv_folder, ret):
        conv_nodes_file = os.path.join(conv_folder, cls.nodes_filename)
        return ConversationNodes.from_file(conv_nodes_file, ret)
    
    @classmethod
    def put_conv_nodes_obj(cls, conv_folder, conv_nodes_obj):
        nodes_file_path = os.path.join(conv_folder, cls.nodes_filename)
        conv_nodes_obj.to_file(nodes_file_path)



class ConversationManager:
    conversation_manager_instance = None

    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS session_info (
            session_id TEXT PRIMARY KEY,
            owner_username TEXT NOT NULL,
            conversation_folder TEXT NOT NULL
        )
    '''

    query_all_session_sql =  '''
        SELECT session_id, conversation_folder, owner_username 
        FROM session_info 
    '''

    query_session_sql =  '''
        SELECT session_id, conversation_folder, owner_username 
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

    def __init__(self, session_db_path: str, conversation_store_root: str) -> None:
        if ConversationManager.conversation_manager_instance is not None:
            return
        self.session_db_path = session_db_path
        self.conversation_store_root = conversation_store_root
        sqlite_connect_and_execute(self.session_db_path, self.create_table_sql)
        ConversationManager.user_manager_instance = self
    
    def add_conversation_info(self, session_id, owner_username, all_submitted_content, socketio):
        conversation_folder = os.path.join(self.conversation_store_root, owner_username, session_id)
        # build folder and insert to db 
        sqlite_connect_and_execute(
            self.session_db_path,
            self.insert_session_sql,
            args=(session_id, owner_username, conversation_folder)
        )
        os.makedirs(conversation_folder)
        
        # save abst file to folder
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
        ConversationFolderStructure.put_conv_abst_obj(conversation_folder, conv_abst)

        # create nodes
        all_content_nodes = []
        num_nodes_to_create = 2 + len(all_submitted_content["uploaded_files"]) + len(all_submitted_content["entered_links"])
        num_nodes_created = 0

        # add user input first
        all_content_nodes.append(ContentNode(
            node_id = str(uuid.uuid4()),
            level = 0,
            valid = True,
            node_type = "I",
            name = all_submitted_content["user_input"],
            note = all_submitted_content["selected_process_function"],
        ))
        num_nodes_created += 1
        socketio.emit('main_submit_progress_update', 
            {'current': num_nodes_created, 'total': num_nodes_to_create,
            'message': f'Start processing user instruction content node.', "level": "info"}
        )

        # process the files and links
        input_material_folder = os.path.join(conversation_folder, ConversationFolderStructure.input_material_folder_name)
        os.makedirs(input_material_folder)
        os.makedirs(os.path.join(conversation_folder, ConversationFolderStructure.output_material_folder_name))
        for upfile in all_submitted_content["uploaded_files"]:
            num_nodes_created += 1
            socketio.emit('main_submit_progress_update', 
                {'current': num_nodes_created, 'total': num_nodes_to_create,
                'message': f'Start processing material node: {upfile.filename} ', "level": "info"}
            )
            save_upfile_path = os.path.join(input_material_folder, upfile.filename)
            try:
                upfile.save(save_upfile_path)
                all_content_nodes.append(ContentNode(
                    node_id = str(uuid.uuid4()),
                    level = 0,
                    valid = True,
                    node_type = "M",
                    name = upfile.filename,
                    source={"tool": "FrontendUploader", "args": None},
                    mime_type = upfile.mimetype,
                    note = f"source:FrontendUploader({upfile.__str__()})",
                    related_file_path = save_upfile_path,
                ))
            except Exception as e:
                all_content_nodes.append(ContentNode(
                    node_id = str(uuid.uuid4()),
                    level = 0,
                    valid = False,
                    node_type = "M",
                    name = upfile.filename,
                    source={"tool": "FrontendUploader", "args": None},
                    note = f"File save error: {upfile.__str__()} ; The reason is {e.__str__()}"
                ))
                socketio.emit('main_submit_progress_update', 
                    {'current': num_nodes_created, 'total': num_nodes_to_create,
                    'message': f"File save error: {upfile.__str__()} ; The reason is {e.__str__()}",
                    "level": "error"}
                )
        
        for elink in all_submitted_content["entered_links"]:
            num_nodes_created += 1
            socketio.emit('main_submit_progress_update', 
                {'current': num_nodes_created, 'total': num_nodes_to_create,
                'message': f'Start processing material node: {elink} ', "level": "info"}
            )
            try:
                response = requests.head(elink)
                file_save_name = wget.download(
                    url=elink, 
                    out=input_material_folder, 
                    bar=lambda current_size, total_size, width: socketio.emit('main_submit_progress_update', {'current': num_nodes_created + 1.0 * current_size/ total_size, 'total': num_nodes_to_create, 'message': "none"})
                )
                all_content_nodes.append(ContentNode(
                    node_id = str(uuid.uuid4()),
                    level = 0,
                    valid = True,
                    node_type = "M",
                    name = os.path.basename(file_save_name), 
                    source={"tool": "WgetDownloader", "args": (elink, )},
                    mime_type = response.headers.get('Content-Type'),
                    note = f"source:WgetDownloader({elink})",
                    related_file_path = file_save_name,
                ))
            except Exception as e:
                all_content_nodes.append(ContentNode(
                    node_id = str(uuid.uuid4()),
                    level = 0,
                    valid = False,
                    node_type = "M",
                    name = elink,
                    source={"tool": "WgetDownloader", "args": (elink, )},
                    note = f"Link parse error: {elink} ; The reason is {e.__str__()}"
                ))
                socketio.emit('main_submit_progress_update', 
                    {'current': num_nodes_created, 'total': num_nodes_to_create,
                    'message': f"Link parse error: {elink} ; The reason is {e.__str__()}",
                    "level": "error"}
                )

        
        # save nodes file to folder
        nodes_obj = ConversationNodes(nodes=all_content_nodes, edges=[])
        ConversationFolderStructure.put_conv_nodes_obj(conversation_folder, nodes_obj)
        

    
    def get_conversation_abstract(self, conversation_folder):
        # get abst from folder
        return ConversationFolderStructure.get_conv_abst_obj(conversation_folder)
    

    def get_session_info_by_id(self, session_id, current_user):
        username = current_user.username
        owner, conv_folder = sqlite_connect_and_execute(
            self.session_db_path, 
            self.query_session_by_id_sql,
            args=(session_id,),
            fetch="one"
        )
        if owner == username or current_user.has_view_shared_permission():
            conv_nodes_file = os.path.join(conv_folder, ConversationFolderStructure.nodes_filename)
            try:
                conv_nodes_file_content = ConversationFolderStructure.get_conv_nodes_obj(conv_folder, ret="dict")
                return {
                    "code": 0,
                    "is_owner": owner == username,
                    "conv_folder": conv_folder, 
                    "conv_nodes_file_content": conv_nodes_file_content
                }
            except Exception as e:
                return {"code": -2, "reason": e.__str__()}

        else:
            return {"code": -1, "reason": "No Permission."}


    
    def delete_conversation_info(self, session_id, current_user):
        # delete folder (including abst, inpt, otpt and everything) and remove from db
        username = current_user.username
        owner, conv_folder = sqlite_connect_and_execute(
            self.session_db_path, 
            self.query_session_by_id_sql,
            args=(session_id,),
            fetch="one"
        )
        if owner == username or current_user.has_delete_all_permission():
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
    
    def take_intelligence_step(self, session_id, username, selected_node_ids, user_input, socketio):
        owner, conv_folder = sqlite_connect_and_execute(
            self.session_db_path, 
            self.query_session_by_id_sql,
            args=(session_id,),
            fetch="one"
        )
        if owner == username:
            conv_abst_obj = ConversationFolderStructure.get_conv_abst_obj(conv_folder)
            conv_nodes_obj = ConversationFolderStructure.get_conv_nodes_obj(conv_folder, ret="obj")
            intelligence_manager = IntelligenceManger(conv_abst_obj, conv_nodes_obj, socketio)
            intelligence_manager.step(selected_node_ids, user_input)
            conv_abst_obj, conv_nodes_obj = intelligence_manager.export()
            # save objs
            ConversationFolderStructure.put_conv_abst_obj(conv_folder, conv_abst_obj)
            ConversationFolderStructure.put_conv_nodes_obj(conv_folder, conv_nodes_obj)
            # ret for rendering new page
            return {
                "code": 0, 
                "conv_folder": conv_folder, 
                "conv_nodes_file_content": ConversationFolderStructure.get_conv_nodes_obj(conv_folder, ret="dict"),
            }
        else:
            return {"code": -1, "reason": "No permission to take step, therefore the input box is banned."}

    
    def get_conversations_by_username(self, current_user):
        username = current_user.username

        if current_user.has_view_all_permission():
            rows = sqlite_connect_and_execute(
                self.session_db_path,
                self.query_all_session_sql,
                fetch="all"
            )
        else:
            rows = sqlite_connect_and_execute(
                self.session_db_path, 
                self.query_session_sql,
                args=(username,),
                fetch="all"
            )
        if rows:
            all_session_info = []
            for row in rows:
                session_id, conversation_folder, owner_username = row
                conv_abst = self.get_conversation_abstract(conversation_folder)
                all_session_info.append(
                    SessionInfo(conv_abst, session_id, owner_username)
                )
            all_session_info.sort(key=lambda session: session.conv_abst.ctime, reverse=True)
            return all_session_info

        else:
            return []
        
        
