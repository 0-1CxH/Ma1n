import uuid
from ..backend.defines import ConversationAbstract, ConversationNodes, ContentNode, ContentEdge

class IntelligenceManger:
    def __init__(self, conv_abst_obj, conv_nodes_obj, socketio):
        self.conv_abst_obj = conv_abst_obj
        self.conv_nodes_obj = conv_nodes_obj
        self.socketio = socketio
        print(self.conv_abst_obj, self.conv_nodes_obj)
    
    def send_by_socketio(self, content):
        self.socketio.emit(
            "intelligence_step_progress_update",
            content
        )

    def step(self, selected_node_ids, user_input, reset_node):
        import time
        print(selected_node_ids, user_input, reset_node)
        for i in range(5):
            self.send_by_socketio({"obj": "pbar", "current": i, "total": 5})
            time.sleep(1)
        if self.conv_nodes_obj.get_max_level() < 10:
            self.conv_abst_obj.title = f"Mock of {self.conv_nodes_obj.get_max_level()}"
            lv =self.conv_nodes_obj.get_max_level() + 1
            for _ in range(self.conv_nodes_obj.get_max_level()+1):
                mock_response = ContentNode(
                    node_id = str(uuid.uuid4()),
                    level = lv,
                    valid=True,
                    node_type="R",
                    name="here is a mock of response.",
                    intelligence_processed=True,
                    note=f"{_+1}/{self.conv_nodes_obj.get_max_level()+1}",
                    source={"tool": "FixedRespOrLLMResp", "args": ("input prompt", ) }
                )
                self.conv_nodes_obj.nodes.append(mock_response)
            mock_artiface = ContentNode(
                node_id = str(uuid.uuid4()),
                level = lv ,
                valid=True,
                node_type="A",
                mime_type="text/code",
                name=f"artifact{lv}.file",
                note="This is the mock of generation messages",
                related_file_path="x/xxx/xx",
                intelligence_processed=True
            )
            self.conv_nodes_obj.nodes.append(mock_artiface)

    
    def export(self):
        return self.conv_abst_obj, self.conv_nodes_obj
