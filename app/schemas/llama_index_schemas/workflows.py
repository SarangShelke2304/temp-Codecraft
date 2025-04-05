from uuid import UUID
from typing import Dict, List
import json
from app.schemas.llama_index_schemas.nodes import Node
from app.schemas.llama_index_schemas.connections import Connection
from dataclasses import dataclass

@dataclass
class ParsedWorkflow:
    workflow_id: UUID
    workflow_name: str
    nodes: Dict[str, Node]
    connections: List[Connection]

    def prettify(self) -> str:
        workflow_dict = {
            "workflow_id": str(self.workflow_id),
            "workflow_name": self.workflow_name,
            "nodes": {node_id: node.prettify() for node_id, node in self.nodes.items()},
            "connections": [conn.prettify() for conn in self.connections]
        }
        return json.dumps(workflow_dict, indent=4)
