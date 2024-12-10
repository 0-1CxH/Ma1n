import uuid
import os
import wget
import requests
from abc import abstractmethod
from ..backend.defines import ContentNode



class BaseTool:
    @abstractmethod
    def __init__(self, **kwargs) -> None:
        pass
    
    @abstractmethod
    def _default_node(self) -> ContentNode:
        pass

    @abstractmethod
    def _execute(self) -> ContentNode:
        pass

    @classmethod
    def execute(cls, **kwargs):
        tool_obj = cls(**kwargs)
        try:
            node = tool_obj._execute()
            node.valid = True
        except Exception as e:
            node = tool_obj._default_node()
            node.valid = False
            node.note = e.__str__()
        node.node_id = str(uuid.uuid4())
        node.level = kwargs["node_level"]
        return node
    
    @classmethod
    def reset_node(cls, node: ContentNode) -> ContentNode:
        pass

    @classmethod
    def regenerate_node(cls, node: ContentNode) -> ContentNode:
        pass


class InputTool(BaseTool):
    def __init__(self, **kwargs) -> None:
        self.tool_name = kwargs.get("tool_name")
        self.input_content = kwargs.get("input_content")
        self.note_content = kwargs.get("note_content")
    
    def _execute(self) -> ContentNode:
        return ContentNode(
            name=self.input_content,
            node_type="I",
            source={"tool": self.tool_name},
            note=self.note_content,
        )
    
    def _default_node(self) -> ContentNode:
        return self._execute()
    

class FrontendFileUploader(BaseTool):
    def __init__(self, **kwargs) -> None:
        self.file_store_obj = kwargs.get("file_store_obj")
        self.file_save_path = kwargs.get("file_save_path")
    
    def _execute(self) -> ContentNode:
        self.file_store_obj.save(self.file_save_path)
        return ContentNode(
            name=self.file_store_obj.filename,
            node_type="M",
            source={"tool": self.__class__.__name__},
            mime_type=self.file_store_obj.mimetype,
            note="",
            related_file_path = self.file_save_path,
        )
    
    def _default_node(self) -> ContentNode:
        return ContentNode(
            name=self.file_store_obj.filename,
            node_type="M",
            source={"tool": self.__class__.__name__},
        )
        

class WgetDownloader(BaseTool):
    def __init__(self, **kwargs) -> None:
        self.link = kwargs.get("link")
        self.save_to_folder = kwargs.get("save_to_folder")
        self.custom_progress_callback = kwargs.get("custom_progress_callback")
    
    def _execute(self) -> ContentNode:
        response = requests.head(self.link)
        file_save_name = wget.download(
            url = self.link,
            out = self.save_to_folder,
            bar = self.custom_progress_callback
        )
        return ContentNode(
            name= os.path.basename(file_save_name),
            node_type="M",
            source={"tool": self.__class__.__name__, "args": {"link": self.link, "save_to_folder": self.save_to_folder}},
            mime_type=response.headers.get('Content-Type'),
            note="",
            related_file_path=file_save_name,
        )
    
    def _default_node(self) -> ContentNode:
        return ContentNode(
            name="(null)",
            node_type="M",
            source={"tool": self.__class__.__name__, "args": {"link": self.link, "save_to_folder": self.save_to_folder}},
            mime_type="(null)",
        )





TOOL_ENTRY = {
    "FrontendInitialInput": InputTool,
    "FrontendFileUploader": FrontendFileUploader,
    "WgetDownloader": WgetDownloader,

}
