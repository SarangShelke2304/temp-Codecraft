from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate
from app.db.session import async_session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.future import select
from app.engine import engine
import uuid

async def create_workflow(workflow: WorkflowCreate):
    async with async_session() as session:
        new_workflow = Workflow(
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
        result = await session.execute(select(Workflow).filter(Workflow.workflow_id == workflow_id))
        return result.scalars().first()

async def update_workflow(workflow_id: uuid.UUID, workflow: WorkflowUpdate):
    async with async_session() as session:
        result = await session.execute(select(Workflow).filter(Workflow.workflow_id == workflow_id))
        wf = result.scalars().first()
        if wf:
            wf.dsl_file = dict(workflow.dsl_file)
            wf.updated_at = workflow.updated_at
            await session.commit()

async def delete_workflow(workflow_id: uuid.UUID):
    async with async_session() as session:
        result = await session.execute(select(Workflow).filter(Workflow.workflow_id == workflow_id))
        wf = result.scalars().first()
        if wf:
            await session.delete(wf)
            await session.commit()

async def start_workflow_execution(workflow_id: uuid.UUID):
    # Simulate starting workflow execution and generating an execution ID
    async with async_session() as session:
        workflow = await session.execute(select(Workflow).filter(Workflow.workflow_id == workflow_id))
        wf = workflow.scalars().first()
        dsl_file = wf.dsl_file
        result = await engine.parse_and_get_order(dsl_file)
        await session.commit()
    return {"message": "Execution started", "execution_id": 123, "Response": result}

async def get_execution_status(workflow_id: uuid.UUID, execution_id: uuid.UUID):
    # Simulate checking execution status
    return "50% completed"

async def retry_execution(workflow_id: uuid.UUID, execution_id: uuid.UUID):
    # Simulate retrying execution and generating new execution ID
    async with async_session() as session:
        workflow = await session.execute(select(Workflow).filter(Workflow.workflow_id == workflow_id))
        wf = workflow.scalars().first()
        dsl_file = wf.dsl_file
        result = await engine.parse_and_get_order(dsl_file)
        await session.commit()
    return {"message": "Retrying", "new_execution_id": 124}
