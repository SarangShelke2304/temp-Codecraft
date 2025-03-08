import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from uuid import UUID


@dataclass
class NodeConfig:
    path: Optional[str] = None
    defaultValue: Optional[str] = None
    store_messages: Optional[str] = None
    x_coordinate: Optional[int] = None
    y_coordinate: Optional[int] = None
    sessionID: Optional[str] = None
    filepath: Optional[str] = None
    fileText: Optional[str] = None
    fileBase64: Optional[str] = None
    fileType: Optional[str] = None
    modelName: Optional[str] = None
    temperature: Optional[float] = None
    input: Optional[str] = None
    system_message: Optional[str] = None
    maximum_tokens: Optional[str] = None
    API_key: Optional[str] = None


@dataclass
class Node:
    type: str
    id: str
    config: NodeConfig
    inputs: List[str]
    outputs: List[str]


@dataclass
class Connection:
    from_node: str
    from_output: str
    to_node: str
    to_input: str


@dataclass
class Workflow:
    workflow_id: UUID
    workflow_name: str
    nodes: Dict[str, Node]
    connections: List[Connection]


class WorkflowParser:
    @staticmethod
    def parse(__json__) -> Workflow:
        # with open(__json__, 'r') as f:
        #     workflow_data = json.load(f)
        workflow_data = __json__
            # print(workflow_data)
        # workflow_data = data['workflow']
        # print(workflow_data['nodes'])
        # Parse nodes
        nodes = {}
        for nodeName, node_data in workflow_data['nodes'].items():
            nodes[nodeName] = Node(
                type=node_data['type'],
                id=node_data['id'],
                config=NodeConfig(**node_data.get('config', {})),
                inputs=node_data.get('inputs', []),
                outputs=node_data.get('outputs', [])
            )

        # for node_name, node in nodes.items():
        #     print(f"Node name: {node_name}, type: {node.type}")
        # Parse connections
        connections = []
        for connection in workflow_data['connections']:
            connections.append(Connection(
                from_node=connection['from']['node'],
                from_output=connection['from']['output'],
                to_node=connection['to']['node'],
                to_input=connection['to']['input']
            ))

        return Workflow(
            workflow_id=UUID(workflow_data['workflow_id']),
            workflow_name=workflow_data['workflow_name'],
            nodes=nodes,
            connections=connections
        )


def parse_dsl_file(__json__):
    parser = WorkflowParser()
    workflow = parser.parse(__json__)
    return workflow

# Usage example
# if __name__ == "__main__":
#     parser = WorkflowParser()
#     workflow = parser.parse(r"D:\temp-codecraft\DSL2.json")
#
#     # Example: Print all node types
#     for node_name, node in workflow.nodes.items():
#         print(f"Node {node_name}: {node.type}")
#
#     # Example: Print all connections
#     for conn in workflow.connections:
#         print(f"Connection: {conn.from_node}.{conn.from_output} -> {conn.to_node}.{conn.to_input}")