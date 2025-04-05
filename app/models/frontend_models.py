from sqlalchemy import Column, String, DateTime, Text, UUID, ForeignKey, INT, Boolean
from sqlalchemy.dialects.postgresql import JSON
from app.db.base import Base
from datetime import datetime
import uuid

class _Components(Base):
    __tablename__ = 'Panel_components'
    node_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    label = Column(String, index=True)
    header = Column(String, index=True)
    order = Column(INT, index=True)
    asset_id = Column(UUID, ForeignKey("Assets.asset_id"), index=True)
    header_order = Column(INT, index=True)

class _Assets(Base):
    __tablename__ = 'Assets'
    asset_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    node_name = Column(String, index=True)

class _Configs(Base):
    __tablename__ = 'Configs'
    config_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID, ForeignKey("Assets.asset_id"), index=True)
    property_name = Column(String, index=True)
    property_type = Column(String, index=True)
    visibility = Column(Boolean, index=True)

class _PropertyTypes(Base):
    __tablename__ = 'PropertyTypes'
    property_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    config_id = Column(UUID, ForeignKey("Configs.config_id"),index=True)
    property_value = Column(String, index=True)
    property_type = Column(String, index=True)