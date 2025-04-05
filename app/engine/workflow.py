import base64
from io import BytesIO
from llama_index.core.workflow import Workflow, step
from llama_index.core.schema import Document
from uuid import UUID
from app.models.workflow import Executions, WorkflowModel
from app.schemas.llama_index_schemas.workflows import ParsedWorkflow
from app.schemas.llama_index_schemas.connections import Connection
from app.schemas.llama_index_schemas.nodes import Node, NodeConfig
from app.schemas.llama_index_schemas.events import ParseDsl, GettingOrder, ExecuteDAG, ExecuteEngine,Response
from app.db.session import async_session
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified
from app.engine.dag import dag
from app.engine.tools import ToolExecutor
from typing import Dict, Any
import uuid

def fix_base64_padding(encoded_data):
    missing_padding = len(encoded_data) % 4
    if missing_padding:
        encoded_data += "=" * (4 - missing_padding)
    return encoded_data

class _Workflow(Workflow):
    def __init__(self):
        super().__init__()
        self.chat_memory_buffer : Dict[uuid.UUID, Any] = {}
        self.human_response: str = None
        self.ai_response: str = None

    @step
    async def parse_dsl(self, ev: ParseDsl) -> GettingOrder:
        workflow_data = ev.dsl
        execution_id=ev.execution_id
        nodes = {}
        document = Document()
        for nodeName, node_data in workflow_data['nodes'].items():
            nodes[nodeName] = Node(
                type=node_data['type'],
                id=node_data['id'],
                config=NodeConfig(**node_data.get('config', {})),
                inputs=node_data.get('inputs', []),
                outputs=node_data.get('outputs', [])
            )
            if node_data['type']=='File':
                encoded = node_data['config']['fileBase64']
                document = Document(
                    text=encoded,
                    metadata={"file_type":"base64", "step":"initial"}
                )

        connections = []
        for connection in workflow_data['connections']:
            connections.append(Connection(
                from_node=connection['from']['node'],
                from_output=connection['from']['output'],
                to_node=connection['to']['node'],
                to_input=connection['to']['input']
            ))

        parsed_workflow = ParsedWorkflow(
            workflow_id=UUID(workflow_data['workflow_id']),
            workflow_name=workflow_data['workflow_name'],
            nodes=nodes,
            connections=connections
        )

        return GettingOrder(parsed_workflow=parsed_workflow, execution_id=execution_id, document=document)

    @step
    async def get_nodes_and_connections(self, ev: GettingOrder) -> ExecuteDAG:
        wf = ev.parsed_workflow
        nodes = wf.nodes
        connections = wf.connections
        execution_id = ev.execution_id
        return ExecuteDAG(nodes_and_connections={'nodes':nodes, 'connections':connections}, execution_id=execution_id, document=ev.document)

    @step
    async def execute_dag(self, ev: ExecuteDAG) -> ExecuteEngine:
        nodes = ev.nodes_and_connections['nodes']
        connections = ev.nodes_and_connections['connections']
        order = await dag(nodes, connections)
        execution_id = ev.execution_id
        # print(nodes)
        return ExecuteEngine(order=order, nodes=nodes, connections=connections, execution_id=execution_id, document=ev.document)

    @step
    async def execute_tools(self, ev: ExecuteEngine) -> Response:
        base64_data = ev.document.text
        try:
            if "," in base64_data:
                _, encoded_data = base64_data.split(",", 1)
            else:
                encoded_data = base64_data

            # Ensure proper padding
            encoded_data = encoded_data.strip().replace("\n", "").replace("\r", "")
            encoded_data = fix_base64_padding(encoded_data)

            decoded_file = base64.b64decode(encoded_data)
            text_file = BytesIO(decoded_file)
            text_content = text_file.read().decode("utf-8", errors="ignore")

        except Exception as e:
            raise Exception(f"Error decoding file: {str(e)}")

        doc = Document(text=text_content, metadata={"file_type":"text"})
        for node, node_data in ev.nodes.items():
            if node_data.type.lower().startswith('chat') or node_data.type.lower().startswith('text'):
                self.human_response = node_data.config.Text if hasattr(node_data.config, 'Text') else None
        _ToolExecutor=ToolExecutor()
        response = await _ToolExecutor.execute_tools(order=ev.order, nodes=ev.nodes, connections=ev.connections, execution_id=ev.execution_id, doc=doc)
        self.ai_response = response.response if hasattr(response, 'response') else None
        self.chat_memory_buffer[ev.execution_id] = [{'human': self.human_response, 'ai': self.ai_response}] 
        async with async_session() as session:
            to_be_updated = await session.execute(select(Executions).filter(Executions.execution_id == ev.execution_id))
            execution = to_be_updated.scalars().first()
            if execution:
                # print(self.chat_memory_buffer[ev.execution_id])
                execution.chat_memory_buffer = self.chat_memory_buffer[ev.execution_id]
                # print(execution.chat_memory_buffer, "\n\n\nExecuted to db")	
                await session.commit()
        return Response(response=response.response)

async def executor(__json__, execution_id):
    w = _Workflow()
    result = await w.run(dsl=__json__, execution_id=execution_id)
    # print(w.chat_memory_buffer)
    return result


async def chat_engine(workflow_id, execution_id, user_message):
    async with async_session() as session:
        to_be_updated = await session.execute(select(Executions).filter(Executions.execution_id == execution_id))
        execution = to_be_updated.scalars().first()
        chat_memory_buffer = execution.chat_memory_buffer
        workflows = await session.execute(select(WorkflowModel).filter(WorkflowModel.workflow_id == workflow_id))
        wf = workflows.scalars().first()
        dsl_file = wf.dsl_file
        for node, node_data in dsl_file['nodes'].items():
            if node_data['type'].lower() == 'llm':
                configs=NodeConfig(**node_data.get('config', {}))
                break
        # print("-----------------------------------------------")
        # print(configs.modelName)
        # print("-----------------------------------------------")
        executor1 = ToolExecutor()
        user_chat_history = Document(text=str(chat_memory_buffer), metadata={"file":"user chat history"})
        response =await executor1.execute_llm(configs=configs, doc=user_message, arg=user_chat_history)
        # print(execution)
        # print(chat_memory_buffer) 

        current_chat = {'human': user_message, 'ai': response.response}
        chat_memory_buffer.append(current_chat)
        execution.chat_memory_buffer = chat_memory_buffer
        flag_modified(execution, "chat_memory_buffer")
        await session.commit()

        return response.response

        

# import asyncio
# import json
# async def main():
#     w= _Workflow()
#     with open('../../DSL3.json') as f:
#         content = json.loads(f.read())
#     res = await w.run(dsl=content, execution_id='7d9e9c92-45d2-42b3-bd71-8a62148cf0bb')
#     print(res)
# asyncio.run(main())
