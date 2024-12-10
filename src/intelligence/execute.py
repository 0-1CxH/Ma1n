import uuid
from multiprocessing import Pool
from ..backend.defines import ConversationAbstract, ConversationNodes, ContentNode, ContentEdge
from .tools import ToolCaller

class IntelligenceManger:
    def __init__(self, conv_abst_obj, conv_nodes_obj, socketio):
        self.conv_abst_obj = conv_abst_obj
        self.conv_nodes_obj = conv_nodes_obj
        self.socketio = socketio
        self.mproc_pool = Pool(20)
        # print(self.conv_abst_obj, self.conv_nodes_obj)
    
    def send_by_socketio(self, content):
        self.socketio.emit(
            "intelligence_step_progress_update",
            content
        )
    
    def update_pbar_by_socketio(self, current, total):
        self.send_by_socketio({"obj": "pbar", "current": current, "total": total})

    def step(self, selected_node_ids, user_input, reset_node):
        
        # pre process
        # check if file exists, if not set to invalid
        
        print(f"{selected_node_ids=}")
        print(f"{user_input=}")
        print(f"{reset_node=}")

        nodes_by_level = {}
        largest_selected_level = -1 
        max_level = -1

        is_reset_mode = False
        is_append_mode = False
        is_view_mode = False

        for idx, node in enumerate(self.conv_nodes_obj.nodes):
            if reset_node is not None: # reset mode
                is_reset_mode = True
                if node.node_id == reset_node:
                    node.valid = False
            else: # view/append mode
                if selected_node_ids is not None:
                    if node.node_id in selected_node_ids:
                        largest_selected_level = max(largest_selected_level, node.level)
                else:
                    max_level = max(max_level, node.level)
            if node.level not in nodes_by_level:
                nodes_by_level[node.level] = []
            nodes_by_level[node.level].append(node)
        
        if not is_reset_mode: 
            if largest_selected_level == -1:
                selected_node_ids = [_.node_id for _ in nodes_by_level[max_level]]
                largest_selected_level = max_level

                print(f"{largest_selected_level, max_level=}")
        
            if user_input is not None: # append mode 
                is_append_mode = True
                # create I node
                if largest_selected_level not in nodes_by_level:
                    nodes_by_level[largest_selected_level] = []
                nodes_by_level[largest_selected_level] = [ToolCaller.get_tool("FrontendAdditionalInput").execute(
                    node_level=largest_selected_level,
                    input_content=user_input,
                    tool_name="FrontendAdditionalInput",
                    note_content="Process"
                )] + nodes_by_level[largest_selected_level]
                selected_node_ids.append(nodes_by_level[largest_selected_level][0].node_id)
            
            if not is_append_mode:
                is_view_mode = True


        
        print(largest_selected_level, selected_node_ids)
        print(f"{is_reset_mode, is_append_mode, is_view_mode=}")
        
        
        # real process
        # invalid node regenerate 
        for idx, node in enumerate(self.conv_nodes_obj.nodes):
            if not node.valid:
                if node.source is not None:
                    self.conv_nodes_obj.nodes[idx] = ToolCaller.get_tool(node.source["tool"]).replay(
                        node, other_kwargs={}
                    )
        # not intellect processed material, use tool to summary
         
        # new response node if inst not resped
        for node in self.conv_nodes_obj.nodes:
            if node.node_type == "I":
                if node.note == "Process":
                    # use process tool 
                    pass
                else:
                    # use according tools 
                    pass

                # check edges, if no valid output, create new R node
                # link new R node to selected_node_ids
                pass




        # for i in range(5):
        #     self.send_by_socketio({"obj": "pbar", "current": i, "total": 5})
        #     time.sleep(1)
        # if self.conv_nodes_obj.get_max_level() < 10:
        #     self.conv_abst_obj.title = f"Mock of {self.conv_nodes_obj.get_max_level()}"
        #     lv =self.conv_nodes_obj.get_max_level() + 1
        #     for _ in range(self.conv_nodes_obj.get_max_level()+1):
        #         mock_response = ContentNode(
        #             node_id = str(uuid.uuid4()),
        #             level = lv,
        #             valid=True,
        #             node_type="R",
        #             name="here is a mock of response.",
        #             intelligence_processed=True,
        #             note=f"{_+1}/{self.conv_nodes_obj.get_max_level()+1}",
        #             source={"tool": "FixedRespOrLLMResp", "args": ("input prompt", ) }
        #         )
        #         self.conv_nodes_obj.nodes.append(mock_response)
        #     mock_artiface = ContentNode(
        #         node_id = str(uuid.uuid4()),
        #         level = lv ,
        #         valid=True,
        #         node_type="M",
        #         mime_type="text/code",
        #         name=f"artifact{lv}.file",
        #         note="This is the mock of generation messages",
        #         related_file_path="x/xxx/xx",
        #         intelligence_processed=True
        #     )
        #     self.conv_nodes_obj.nodes.append(mock_artiface)

    
    def export(self):
        return self.conv_abst_obj, self.conv_nodes_obj
