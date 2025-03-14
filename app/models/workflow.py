from sqlalchemy import Column, String, DateTime, Text, UUID
from sqlalchemy.dialects.postgresql import JSON
from app.db.base import Base
from datetime import datetime
import uuid

class Workflow(Base):
    __tablename__ = "workflows"

    workflow_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    workflow_name = Column(String, index=True)
    description = Column(Text, nullable=True)
    status = Column(String, default="paused")
    created_at = Column(DateTime(timezone=True), default=lambda:datetime.now())
    updated_at = Column(DateTime(timezone=True), default=lambda:datetime.now(), onupdate=lambda:datetime.now())
    created_by = Column(UUID(as_uuid=True), nullable=True, default=uuid.UUID)
    dsl_file = Column(JSON, nullable=True)  # Now using JSON type

# class Chat(Base):
#     __tablename__ = "chats"
#     chat_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
#     workflow_id = Column(UUID(as_uuid=True), index=True)
#     chat_messages = Column(JSON, nullable=True)
#     created_at = Column(DateTime(timezone=True), default=lambda:datetime.now())