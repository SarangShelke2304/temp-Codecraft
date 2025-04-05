import uuid
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, File
from app.schemas.api_schemas import WorkflowCreate, WorkflowResponse, WorkflowUpdate, ExecutionStatus
from app.crud.workflow import (
    create_workflow, get_workflow, update_workflow, delete_workflow,
    start_workflow_execution, get_execution_status, retry_execution, upload_file, get_all_workflows
)

from app.engine.workflow import chat_engine

router = APIRouter()

# /upload: payload: file  file_executer-> extract text
@router.post("/create", response_model=WorkflowResponse)
async def create_new_workflow(workflow: WorkflowCreate):
    # print(workflow)
    return await create_workflow(workflow)

@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def read_workflow(workflow_id: uuid.UUID):
    workflow = await get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.get("/all/{user_id}", response_model=List[WorkflowResponse])
async def read_all_workflows(user_id:uuid.UUID):
    workflows = await get_all_workflows(user_id)
    return workflows if workflows else []

@router.put("/{workflow_id}", response_model=dict)
async def update_existing_workflow(workflow_id: uuid.UUID, workflow: WorkflowUpdate):
    await update_workflow(workflow_id, workflow)
    return {"message": "Workflow saved successfully"}

@router.delete("/{workflow_id}", response_model=dict)
async def delete_existing_workflow(workflow_id: uuid.UUID):
    await delete_workflow(workflow_id)
    return {"message": "workflow deleted successfully"}

@router.post("/{workflow_id}/start", response_model=dict)
async def start_workflow(workflow_id: uuid.UUID):
    result = await start_workflow_execution(workflow_id)
    return result

@router.get("/{workflow_id}/executions/{execution_id}/status", response_model=ExecutionStatus)
async def check_execution_status(workflow_id: uuid.UUID, execution_id: uuid.UUID):
    status = await get_execution_status(workflow_id, execution_id)
    return {"message": status}

@router.post("/{workflow_id}/executions/{execution_id}/retry", response_model=dict)
async def retry_workflow(workflow_id: uuid.UUID, execution_id: uuid.UUID):
    result = await retry_execution(workflow_id, execution_id)
    return result
#
# @router.post("{workflow_id}/chat/{chat_id}", response_model=dict)
# async def send_message(chat_id: uuid.UUID, user_chat_message: str):
#     response = await chat_response_generator(chat_id, user_chat_message)
#     return {"response": response}

@router.post("{workflow_id}/chat/{chat_id}")
async def send_message(workflow_id: uuid.UUID, chat_id: uuid.UUID, user_message: str):
    response = await chat_engine(workflow_id, chat_id, user_message)
    return {"response": response}

@router.post("/upload", response_model=dict)
async def upload_file_endpoint(workflow_id: uuid.UUID, file: UploadFile = File(...)):
    response = await upload_file(file, workflow_id)
    return response

