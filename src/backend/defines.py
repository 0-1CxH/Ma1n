import os
import json

from dataclasses import dataclass
from typing import List

@dataclass
class ConversationAbstract:
    title: str
    ctime: str
    abst: str
    note: str

    def to_file(self, abst_file):
        with open(abst_file, "w") as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)
    
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
class ContentNode:
    name: str
    node_type: str # M[material], A[artifact], I[instruction], R[response]
    valid: bool = False
    node_id: str = None
    level: int = None
    source: dict = None # {"tool": "", "args": (,), "refs": []}
    mime_type: str = None
    note: str = None
    related_file_path: str = None
    cap_img_path: str = None
    intelligence_processed: bool = False

    # for type I node:
    # name is full instruction
    # note is selected proc func
    # source: indexInput additionalInput resetInput

    # for type M node:
    # name is filename (if valid), or something short (if invalid)
    # note is intelligence summary or generation message  (if invalid, is the error msg)
    # source should not be None, but defines the tool and args for regen
    # mime_type  is the type of file (if valid) or None (if invalid )
    # attach the related_file_path (if valid) or none (if invalid)
    # if want to use llm summary, intelligence_processed is false; else true

    # for type R node:
    # name is full response
    # note is x/y responses in batch
    # source is also required (for regenerate)
    



@dataclass
class ContentEdge:
    source_node_id: str
    target_node_id: str

@dataclass
class ConversationNodes:
    nodes: List[ContentNode]
    edges: List[ContentEdge]

    def get_max_level(self):
        return max([node.level for node in self.nodes])
    
    @classmethod
    def from_file(cls, nodes_file, ret):
        with open(nodes_file) as f:
            conv_nodes_file_content = json.loads(f.read())
            if ret=="dict":
                return conv_nodes_file_content
            elif ret == "obj":
                return ConversationNodes(
                    nodes=[ContentNode(**_) for _ in conv_nodes_file_content["nodes"]],
                    edges=[ContentEdge(**_) for _ in conv_nodes_file_content["edges"]]
                )
    
    def to_file(self, nodes_file):
        with open(nodes_file, "w") as f:
            json.dump({
                "nodes": [n.__dict__ for n in self.nodes],
                "edges": [e.__dict__ for e in self.edges],
                "max_node_level": self.get_max_level(),
            }, f, ensure_ascii=False, indent=4)

