# from app.engine.engine import chat_memory_buffer
import base64
from sqlalchemy.orm.attributes import flag_modified
from app.models.workflow import WorkflowModel, Executions
from app.models.frontend_models import _Components
from app.schemas.api_schemas import WorkflowCreate, WorkflowUpdate, Execution
from app.db.session import async_session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import desc
from app.engine.workflow import executor
import uuid
import datetime

async def create_workflow(workflow: WorkflowCreate):
    async with async_session() as session:
        new_workflow = WorkflowModel(
            workflow_name=workflow.workflow_name,
            description=workflow.description,
            created_by=workflow.created_by,
            dsl_file=workflow.dsl_file
        )
        try:
            session.add(new_workflow)
            await session.commit()
            await session.refresh(new_workflow)
            return new_workflow
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=400,
                detail="workflow name unavailable, choose a different workflow name"
            )

async def get_workflow(workflow_id: uuid.UUID):
    async with async_session() as session:
        result = await session.execute(select(WorkflowModel).filter(WorkflowModel.workflow_id == workflow_id))
        return result.scalars().first()

async def get_all_workflows(user_id: uuid.UUID):
    async with async_session() as session:
        result = await session.execute(select(WorkflowModel).filter(WorkflowModel.created_by == user_id).order_by(desc(WorkflowModel.created_at)))
        return result.scalars().all()

async def update_workflow(workflow_id: uuid.UUID, workflow: WorkflowUpdate):
    async with async_session() as session:
        result = await session.execute(select(WorkflowModel).filter(WorkflowModel.workflow_id == workflow_id))
        wf = result.scalars().first()
        if wf:
            wf.dsl_file = dict(workflow.dsl_file)
            wf.updated_at = workflow.updated_at
            await session.commit()

async def delete_workflow(workflow_id: uuid.UUID):
    async with async_session() as session:
        result = await session.execute(select(WorkflowModel).filter(WorkflowModel.workflow_id == workflow_id))
        wf = result.scalars().first()
        if wf:
            await session.delete(wf)
            await session.commit()

async def start_workflow_execution(workflow_id: uuid.UUID):
    # Simulate starting workflow execution and generating an execution ID
    async with async_session() as session:
        execution = Executions(
            execution_id=uuid.uuid4(),
            workflow_id=workflow_id,
            started_at = datetime.datetime.now()
        )
        try:
            session.add(execution)
            await session.commit()
            await session.refresh(execution)
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=400,
                detail=IntegrityError
            )
        workflow = await session.execute(select(WorkflowModel).filter(WorkflowModel.workflow_id == workflow_id))
        wf = workflow.scalars().first()
        dsl_file = wf.dsl_file
        result = await executor(dsl_file, execution.execution_id)
        await session.commit()
    return {"message": "Execution started", "execution_id": execution.execution_id, "Response": result}

async def get_execution_status(workflow_id: uuid.UUID, execution_id: uuid.UUID):
    # Simulate checking execution status
    return "50% completed"

async def retry_execution(workflow_id: uuid.UUID, execution_id: uuid.UUID):
    # Simulate retrying execution and generating new execution ID
    async with async_session() as session:
        workflow = await session.execute(select(WorkflowModel).filter(WorkflowModel.workflow_id == workflow_id))
        wf = workflow.scalars().first()
        dsl_file = wf.dsl_file
        result = await executor(dsl_file)
        await session.commit()
    return {"message": "Retrying", "new_execution_id": 124, "result": result}

async def upload_file(file, workflow_id: uuid.UUID):
    async with async_session() as session:
        workflow = await session.execute(select(WorkflowModel).filter(WorkflowModel.workflow_id == workflow_id))
        wf = workflow.scalars().first()
        content = await file.read()
        # print(content)
        encoded = base64.b64encode(content).decode('utf-8')
        # print(encoded)
        nodes = wf.dsl_file.get("nodes", {})
        updated = False
        for node_id, node_data in nodes.items():
            if node_data.get("type") == "File":
                node_data["config"]["fileBase64"]=encoded
                updated = True
                break
        if updated:
            flag_modified(wf, "dsl_file")
            session.add(wf)
            await session.commit()
        return {"message": "File uploaded successfully!" if updated else "No 'File' node found!"}


async def get_panel_components():
    async with async_session() as session:
        #get all rows from table "Panel_components"
        result = await session.execute(select(_Components))
        components = result.scalars().all()
        # print(components)
        return components
