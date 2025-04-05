from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime
import uuid

class WorkflowBase(BaseModel):
    workflow_name: str
    description: Optional[str] = None
    created_by: uuid.UUID
    dsl_file: Optional[Dict[Any, Any]] = None

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowUpdate(BaseModel):
    updated_at: datetime
    dsl_file: Dict[Any, Any]

class WorkflowResponse(WorkflowBase):
    workflow_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime
    created_by: uuid.UUID
    dsl_file: Optional[Dict[Any, Any]]

    class Config:
        from_attributes = True

class ExecutionStatus(BaseModel):
    message: str

class Execution(BaseModel):
    execution_id: uuid.UUID
    workflow_id: uuid.UUID
    started_at: datetime
    chat_memory_buffer: Dict[Any, Any]
#
# class ChatBase(BaseModel):
#     chat_id: uuid.UUID
#     workflow_id: uuid.UUID
#     chat_messages: Dict[Any, Any]
