from llama_index.core.workflow import StartEvent, Event, StopEvent
from llama_index.core.schema import Document
from typing import Dict, List, Any
from app.schemas.llama_index_schemas.workflows import ParsedWorkflow
from app.schemas.llama_index_schemas.nodes import Node
from app.schemas.llama_index_schemas.connections import Connection
from uuid import UUID

class ParseDsl(StartEvent):
    dsl: Dict[str, Any]
    execution_id: UUID

class GettingOrder(Event):
    parsed_workflow: ParsedWorkflow
    execution_id: UUID
    document: Document

class ExecuteDAG(Event):
    nodes_and_connections: Dict[str, Any]
    execution_id: UUID
    document: Document

class ExecuteEngine(Event):
    order: List[Any]
    nodes: Dict[str, Node]
    connections: List[Connection]
    execution_id: UUID
    document: Document

class Response(StopEvent):
    response: str